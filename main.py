from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import json
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create FastAPI app with explicit docs configuration
app = FastAPI(
    title="AI Tools Recommender",
    description="API for recommending AI tools based on user descriptions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Load environment variables from .env
load_dotenv()

# Basic CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI tools database
with open("ai_tools.json") as f:
    AI_TOOLS = json.load(f)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"status": "ok", "message": "API is working!"}

@app.get("/test")
async def test():
    logger.debug("Test endpoint called")
    return {"status": "ok", "message": "Test endpoint is working!"}

@app.get("/ping")
async def ping():
    logger.debug("Ping endpoint called")
    return {"status": "ok", "message": "pong"}

@app.post("/recommend")
async def recommend_tools(request: Request):
    logger.debug("Recommend endpoint called")
    data = await request.json()
    description = data.get("description", "")
    return {"recommendations": AI_TOOLS}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) 