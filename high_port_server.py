from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    port = 49152  # Using the same high port that worked in our tests
    print(f"Starting HTTP server on port {port}")
    print(f"Try accessing: http://127.0.0.1:{port}")
    server = HTTPServer(('127.0.0.1', port), SimpleHTTPRequestHandler)
    server.serve_forever() 