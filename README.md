# Simmons Chatbot Backend

A FastAPI backend that recommends AI tools based on a user's business or project description using natural language. The backend leverages OpenAI's GPT-4 to analyze user input and matches needs to a curated database of AI tools.

## Features
- Accepts natural language descriptions of businesses or projects
- Uses OpenAI GPT-4 to analyze user needs
- Recommends relevant AI tools from a customizable database
- Simple REST API for easy integration with any frontend

## Setup

1. **Clone the repository and navigate to the project folder:**
   ```bash
   git clone <your-repo-url>
   cd simmonsChatbot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key:**
   - Create a `.env` file in the project root:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

5. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

## Usage

Send a POST request to the `/recommend` endpoint with a JSON body containing a `description` field:

```bash
curl -X POST "http://127.0.0.1:8000/recommend" \
     -H "Content-Type: application/json" \
     -d '{"description": "I run an e-commerce store and want to automate order tracking."}'
```

**Response:**
```json
{
  "recommendations": [
    {
      "name": "Dialogflow",
      "category": "Chatbot",
      "description": "Build conversational interfaces for customer support.",
      "use_cases": ["customer support", "FAQ automation"]
    },
    {
      "name": "Zapier",
      "category": "Automation",
      "description": "Automate workflows between apps.",
      "use_cases": ["order tracking", "email automation"]
    }
  ]
}
```

## Customizing the AI Tools Database
- Edit `ai_tools.json` to add, remove, or update AI tools.
- Each tool should have a `name`, `category`, `description`, and `use_cases` array.

## Contributing
Pull requests and suggestions are welcome! Please open an issue or submit a PR.

## Troubleshooting
- Ensure your `.env` file is present and contains a valid OpenAI API key.
- If you add new dependencies, update `requirements.txt`.
- For CORS issues, check frontend and backend origins.

## Next Steps
- Integrate OpenAI GPT-4 to analyze user descriptions and match relevant tools.
- Expand the AI tools database for broader recommendations.

## Files
- `main.py`: FastAPI app
- `ai_tools.json`: Sample AI tools database
- `