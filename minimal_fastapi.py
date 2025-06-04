from fastapi import FastAPI
import uvicorn
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    logger.debug("Root endpoint called")
    return {"Hello": "World"}

if __name__ == "__main__":
    try:
        logger.info("Starting FastAPI server...")
        config = uvicorn.Config(
            app,
            host="127.0.0.1",
            port=12345,
            log_level="debug",
            access_log=True
        )
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1) 