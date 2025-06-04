from http.server import HTTPServer, BaseHTTPRequestHandler

class BasicHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Basic server is working!')

def run():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, BasicHandler)
    print('Starting basic server on http://127.0.0.1:8080')
    httpd.serve_forever()

if __name__ == '__main__':
    run() 