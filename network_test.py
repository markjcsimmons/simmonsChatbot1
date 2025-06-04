import socket
import sys
import time
import threading

def run_server(port):
    try:
        # Create a server socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reuse of the address
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Try to bind to the port
        server.bind(('127.0.0.1', port))
        print(f"Server: Successfully bound to port {port}")
        # Start listening
        server.listen(1)
        print(f"Server: Listening on port {port}")
        
        # Accept a connection
        conn, addr = server.accept()
        print(f"Server: Connected by {addr}")
        conn.send(b"Hello from server!")
        conn.close()
        server.close()
    except socket.error as e:
        print(f"Server error: {e}")

def run_client(port):
    time.sleep(1)  # Give server time to start
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout of 5 seconds
        s.settimeout(5)
        # Try to connect
        s.connect(('127.0.0.1', port))
        print(f"Client: Successfully connected to localhost:{port}")
        # Receive data
        data = s.recv(1024)
        print(f"Client: Received: {data.decode()}")
        s.close()
    except socket.error as e:
        print(f"Client error: {e}")

if __name__ == "__main__":
    port = 12345
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()
    
    # Run client in main thread
    run_client(port)
    
    # Wait for server to finish
    server_thread.join()

def test_server_binding(port):
    try:
        # Create a server socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reuse of the address
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Try to bind to the port
        server.bind(('127.0.0.1', port))
        print(f"Successfully bound to port {port}")
        # Start listening
        server.listen(1)
        print(f"Server listening on port {port}")
        server.close()
        return True
    except socket.error as e:
        print(f"Failed to bind to port {port}")
        print(f"Error: {e}")
        return False

def test_connection(host, port):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout of 5 seconds
        s.settimeout(5)
        # Try to connect
        s.connect((host, port))
        print(f"Successfully connected to {host}:{port}")
        s.close()
    except socket.error as e:
        print(f"Failed to connect to {host}:{port}")
        print(f"Error: {e}")

# Test localhost
print("Testing localhost connection...")
test_connection('127.0.0.1', 9000)

# Test a known working website
print("\nTesting connection to google.com...")
test_connection('google.com', 80)

def test_port(port):
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        
        # Try to connect
        result = sock.connect_ex(('127.0.0.1', port))
        
        if result == 0:
            print(f"Port {port} is open and accepting connections")
        else:
            print(f"Port {port} is closed or not accepting connections")
            
        sock.close()
    except Exception as e:
        print(f"Error testing port {port}: {e}")

def test_ports():
    print("Testing common ports...")
    ports = [3000, 8000, 8080, 5000, 9000]
    for port in ports:
        test_port(port)

if __name__ == "__main__":
    print("Starting network connectivity test...")
    test_ports() 