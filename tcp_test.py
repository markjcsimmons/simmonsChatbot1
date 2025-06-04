import socket
import sys
import time
import threading

def run_tcp_server():
    try:
        # Create TCP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reuse of the address
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to the same high port number
        server.bind(('127.0.0.1', 49152))
        print("TCP Server: Started on port 49152")
        
        # Listen for connections
        server.listen(1)
        print("TCP Server: Listening for connections...")
        
        # Accept connection
        conn, addr = server.accept()
        print(f"TCP Server: Connected by {addr}")
        
        # Receive data
        data = conn.recv(1024)
        print(f"TCP Server: Received: {data.decode()}")
        
        # Send response
        conn.send(b"Hello from TCP server!")
        
    except Exception as e:
        print(f"TCP Server error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
        server.close()

def run_tcp_client():
    try:
        # Create TCP socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server
        client.connect(('127.0.0.1', 49152))
        print("TCP Client: Connected to server")
        
        # Send message
        message = "Hello from TCP client!"
        client.send(message.encode())
        print("TCP Client: Sent message")
        
        # Receive response
        data = client.recv(1024)
        print(f"TCP Client: Received: {data.decode()}")
        
    except Exception as e:
        print(f"TCP Client error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("Starting TCP test...")
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_tcp_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Give server time to start
    time.sleep(1)
    
    # Run client
    run_tcp_client()
    
    # Keep main thread alive briefly to see server output
    time.sleep(2) 