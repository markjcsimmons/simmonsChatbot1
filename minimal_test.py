from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import json
import os
from dotenv import load_dotenv
import logging
import uvicorn

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS middleware added")

# Load AI tools database
try:
    with open("ai_tools.json") as f:
        AI_TOOLS = json.load(f)
    logger.info("AI tools database loaded successfully")
except Exception as e:
    logger.error(f"Error loading AI tools database: {e}")
    AI_TOOLS = []

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    logger.error("OpenAI API key not found in environment variables")
else:
    logger.info("OpenAI API key loaded")

@app.get("/")
def read_root():
    logger.debug("Root endpoint called")
    return {"Hello": "World"}

@app.get("/ping")
def ping():
    logger.debug("Ping endpoint called")
    return {"status": "ok", "message": "pong"}

@app.post("/recommend")
async def recommend_tools(request: Request):
    logger.debug("Recommend endpoint called")
    try:
        data = await request.json()
        description = data.get("description", "")
        logger.info(f"Received description: {description}")
        
        # Get recommendations from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that recommends AI tools based on user descriptions."},
                {"role": "user", "content": f"Based on this description: '{description}', which of these AI tools would be most helpful? {json.dumps(AI_TOOLS)}"}
            ]
        )
        recommendations = response.choices[0].message.content
        logger.info("Successfully got recommendations from OpenAI")
        return {"recommendations": recommendations}
    except Exception as e:
        logger.error(f"Error in recommend_tools: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug") 