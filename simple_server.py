from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import json
import os
from dotenv import load_dotenv
import openai
import socket

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load AI tools database
try:
    with open("ai_tools.json") as f:
        AI_TOOLS = json.load(f)
    logger.info("AI tools database loaded successfully")
except Exception as e:
    logger.error(f"Error loading AI tools database: {e}")
    AI_TOOLS = []

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.debug(f"Received request for path: {self.path}")
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Simple server is working!")
        except Exception as e:
            logger.error(f"Error in GET handler: {e}")
            self.send_error(500, str(e))

    def do_POST(self):
        if self.path == '/recommend':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                description = data.get('description', '')
                
                # Get recommendations from OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that recommends AI tools based on user descriptions."},
                        {"role": "user", "content": f"Based on this description: '{description}', which of these AI tools would be most helpful? {json.dumps(AI_TOOLS)}"}
                    ]
                )
                recommendations = response.choices[0].message.content
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"recommendations": recommendations}).encode())
            except Exception as e:
                logger.error(f"Error processing recommendation request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        logger.debug(f"{format % args}")

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == "__main__":
    port = 3000  # Changed to port 3000
    
    # Check if port is in use
    if is_port_in_use(port):
        logger.error(f"Port {port} is already in use")
        exit(1)
    
    try:
        logger.info(f"Starting server on port {port}")
        server = HTTPServer(('127.0.0.1', port), SimpleHandler)
        logger.info(f"Server started at http://127.0.0.1:{port}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        exit(1)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        server.server_close() 