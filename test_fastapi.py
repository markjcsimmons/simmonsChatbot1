from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import json
import os
from dotenv import load_dotenv
import logging
import uvicorn

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

# Load environment variables
load_dotenv()

# Add CORS middleware
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

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/recommend")
async def recommend_tools(request: Request):
    logger.debug("Recommend endpoint called")
    data = await request.json()
    description = data.get("description", "")
    
    # Get recommendations from OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that recommends AI tools based on user descriptions."},
                {"role": "user", "content": f"Based on this description: '{description}', which of these AI tools would be most helpful? {json.dumps(AI_TOOLS)}"}
            ]
        )
        recommendations = response.choices[0].message.content
        return {"recommendations": recommendations}
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("test_fastapi:app", host="127.0.0.1", port=3000, reload=True) 