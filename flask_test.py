from flask import Flask
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    logger.info("Received request to /")
    return "Flask test server is working!"

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(host='127.0.0.1', port=8080, debug=True) 