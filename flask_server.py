from flask import Flask, jsonify
from flask_cors import CORS
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    logger.debug("Home endpoint called")
    return jsonify({"message": "Flask server is working!"})

@app.route('/ping')
def ping():
    logger.debug("Ping endpoint called")
    return jsonify({"status": "ok", "message": "pong"})

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=8080, debug=True) 