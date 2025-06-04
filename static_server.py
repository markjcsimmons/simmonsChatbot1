from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    port = 8000
    print(f"Starting static file server on port {port}")
    print(f"Try accessing: http://localhost:{port}")
    server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    server.serve_forever() 