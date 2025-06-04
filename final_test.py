from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import json
import os
import traceback
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not api_key:
    logger.error("OpenAI API key not found in environment variables")
    raise ValueError("OpenAI API key not found in environment variables")
if not supabase_url or not supabase_key:
    logger.error("Supabase credentials not found in environment variables")
    raise ValueError("Supabase credentials not found in environment variables")

# Initialize clients
client = OpenAI(api_key=api_key)
supabase = create_client(supabase_url, supabase_key)
logger.info("OpenAI API key loaded")
logger.info("Supabase client initialized")

# Load AI tools from Supabase
try:
    response = supabase.table('ai_tools').select('*').execute()
    AI_TOOLS = response.data
    logger.info(f"Loaded {len(AI_TOOLS)} AI tools from Supabase")
except Exception as e:
    logger.error(f"Error loading AI tools from Supabase: {e}")
    # Fallback to local JSON file
    try:
        with open('ai_tools.json', 'r') as f:
            AI_TOOLS = json.load(f)
        logger.info(f"Loaded {len(AI_TOOLS)} AI tools from local file")
    except Exception as e:
        logger.error(f"Error loading AI tools from local file: {e}")
        AI_TOOLS = []

# Extract unique categories from AI tools
CATEGORIES = sorted(list(set(tool['category'] for tool in AI_TOOLS)))
logger.info(f"Available categories: {CATEGORIES}")

class SimpleHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '3600')

    def do_GET(self):
        logger.debug(f"Received GET request for path: {self.path}")
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self._set_cors_headers()
                self.end_headers()
                with open('test_form.html', 'rb') as f:
                    self.wfile.write(f.read())
            elif self.path.startswith('/tools'):
                # Parse query parameters
                from urllib.parse import urlparse, parse_qs
                query = parse_qs(urlparse(self.path).query)
                category = query.get('category', [''])[0]
                
                # Get tools that match the category or have related use cases/descriptions
                tools = []
                for tool in AI_TOOLS:
                    # Check multiple criteria for relevance
                    is_relevant = (
                        # Exact category match
                        tool['category'].lower() == category.lower() or
                        # Category in use cases
                        any(category.lower() in use_case.lower() for use_case in tool['use_cases']) or
                        # Category in description
                        category.lower() in tool['description'].lower() or
                        # Related categories (e.g., "Content Creation" is related to "Copywriting")
                        any(related in tool['category'].lower() for related in [
                            'content', 'writing', 'creation', 'generation', 'editing'
                        ] if category.lower() in ['content creation', 'copywriting', 'writing assistant'])
                    )
                    
                    if is_relevant:
                        # Add relevance score and type
                        tool_with_metadata = tool.copy()
                        if tool['category'].lower() == category.lower():
                            tool_with_metadata['relevance_type'] = 'primary'
                            tool_with_metadata['relevance_score'] = 1.0
                        else:
                            tool_with_metadata['relevance_type'] = 'related'
                            tool_with_metadata['relevance_score'] = 0.7
                        tools.append(tool_with_metadata)
                
                # Sort tools by relevance score
                tools.sort(key=lambda x: x['relevance_score'], reverse=True)
                
                logger.info(f"Found {len(tools)} tools for category: {category}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(tools).encode())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b"Final test server is working!")
        except Exception as e:
            logger.error(f"Error in GET handler: {e}\n{traceback.format_exc()}")
            self.send_error(500, str(e))

    def do_POST(self):
        logger.debug(f"Received POST request for path: {self.path}")
        if self.path == '/recommend':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                description = data.get('description', '')
                logger.info(f"Received description: {description}")
                
                # Get recommendations from OpenAI
                logger.debug("Calling OpenAI API...")
                try:
                    logger.debug(f"Using API key: {api_key[:5]}...")  # Log first 5 chars of API key
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": f"You are a helpful assistant that recommends AI tool categories. Choose 5-7 categories from this list: {', '.join(CATEGORIES)}. Consider both primary and related categories that could be useful. Return each category on a new line in the format 'Category: [category name]'."},
                            {"role": "user", "content": f"Based on this description: '{description}', what are the 5-7 most relevant AI tool categories from this list: {', '.join(CATEGORIES)}? Consider both primary and related categories that could be useful. Return each category on a new line in the format 'Category: [category name]'."}
                        ],
                        temperature=0.8,
                        max_tokens=500
                    )
                    recommendations = response.choices[0].message.content
                    logger.info("Successfully got recommendations from OpenAI")
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self._set_cors_headers()
                    self.end_headers()
                    response_data = {"recommendations": recommendations}
                    logger.debug(f"Sending response: {response_data}")
                    self.wfile.write(json.dumps(response_data).encode())
                except Exception as api_error:
                    error_traceback = traceback.format_exc()
                    logger.error(f"OpenAI API error: {str(api_error)}\n{error_traceback}")
                    error_response = {"error": f"OpenAI API error: {str(api_error)}"}
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self._set_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response).encode())
            except Exception as e:
                error_traceback = traceback.format_exc()
                logger.error(f"Error processing recommendation request: {str(e)}\n{error_traceback}")
                error_response = {"error": f"Server error: {str(e)}"}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self._set_cors_headers()
            self.end_headers()

    def do_OPTIONS(self):
        logger.debug("Received OPTIONS request")
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

if __name__ == "__main__":
    port = 49152
    logger.info(f"Starting server on port {port}")
    logger.info(f"Try accessing: http://127.0.0.1:{port}")
    server = HTTPServer(('127.0.0.1', port), SimpleHandler)
    server.serve_forever() 