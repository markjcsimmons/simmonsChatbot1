import socket
import sys
import time
import threading

def run_udp_server():
    try:
        # Create UDP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to a high port number
        server.bind(('127.0.0.1', 49152))
        print("UDP Server: Started on port 49152")
        
        while True:
            # Receive data
            data, addr = server.recvfrom(1024)
            print(f"UDP Server: Received from {addr}: {data.decode()}")
            # Send response
            server.sendto(b"Hello from UDP server!", addr)
            
    except Exception as e:
        print(f"UDP Server error: {e}")
    finally:
        server.close()

def run_udp_client():
    try:
        # Create UDP socket
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Send message
        message = "Hello from UDP client!"
        client.sendto(message.encode(), ('127.0.0.1', 49152))
        print("UDP Client: Sent message")
        
        # Receive response
        data, addr = client.recvfrom(1024)
        print(f"UDP Client: Received from {addr}: {data.decode()}")
        
    except Exception as e:
        print(f"UDP Client error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("Starting UDP test...")
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_udp_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Give server time to start
    time.sleep(1)
    
    # Run client
    run_udp_client()
    
    # Keep main thread alive briefly to see server output
    time.sleep(2) 