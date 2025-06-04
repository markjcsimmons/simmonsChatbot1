from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            logger.debug(f"Received request for path: {self.path}")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Server is working!')
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            self.send_error(500, str(e))

def run(port=3000):
    try:
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, SimpleHandler)
        logger.info(f'Starting server on http://127.0.0.1:{port}')
        httpd.serve_forever()
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run() 