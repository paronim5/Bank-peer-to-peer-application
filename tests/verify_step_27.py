import socket
import subprocess
import time
import os
import signal
import sys

HOST = "127.0.0.1"
PORT = 65525
DB_FILE = "bank_data.json"

def run_command(sock, command):
    sock.sendall((command + "\n").encode('utf-8'))
    response = sock.recv(1024).decode('utf-8').strip()
    return response

def verify():
    print("--- Starting Verification Step 27 ---")
    
    # 1. Clean up previous data
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed existing {DB_FILE}")

    # 2. Start Server
    print("Starting Server...")
    # Use sys.executable to ensure we use the same python interpreter
    server_process = subprocess.Popen([sys.executable, "bank_node/main.py"], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE)
    
    try:
        time.sleep(3) # Give it time to start
        
        # 3. Connect and Test
        print("Connecting to server...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
            # BC
            print("Sending BC...")
            res = run_command(s, "BC")
            print(f"Received: {res}")
            assert "127.0.0.1" in res, f"BC failed: {res}"
            
            # AC
            print("Sending AC...")
            res = run_command(s, "AC")
            print(f"Received: {res}")
            assert "AC" in res, f"AC failed: {res}"
            
            # Parse Account ID from response: AC <account_id>/<ip>
            # Example: AC 61092/127.0.0.1
            try:
                parts = res.split(" ")
                if len(parts) > 1:
                    account_info = parts[1] # 61092/127.0.0.1
                    account_id = account_info.split("/")[0]
                    print(f"Captured Account ID: {account_id}")
                else:
                    raise ValueError("Invalid AC response format")
            except Exception as e:
                print(f"Failed to parse Account ID: {e}")
                # Fallback to hardcoded if needed, but better to fail
                raise

            # AD
            print(f"Sending AD {account_id}/{HOST} 1000...")
            res = run_command(s, f"AD {account_id}/{HOST} 1000")
            print(f"Received: {res}")
            assert "AD" in res, f"AD failed: {res}"
            
            # AB
            print(f"Sending AB {account_id}/{HOST}...")
            res = run_command(s, f"AB {account_id}/{HOST}")
            print(f"Received: {res}")
            assert "1000" in res, f"AB failed: {res}"

    finally:
        print("Stopping Server...")
        server_process.terminate()
        server_process.wait()
        
    print("--- Server Restart Test (Persistence) ---")
    
    # 4. Restart Server
    print("Restarting Server...")
    server_process = subprocess.Popen([sys.executable, "bank_node/main.py"], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE)
    
    try:
        time.sleep(3)
        
        print("Connecting to server...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
            # Check AB again
            print(f"Sending AB {account_id}/{HOST}...")
            res = run_command(s, f"AB {account_id}/{HOST}")
            print(f"Received: {res}")
            assert "1000" in res, f"Persistence failed: {res}"
            
    finally:
        print("Stopping Server...")
        server_process.terminate()
        server_process.wait()

    print("\n✅ Verification Step 27 Passed Successfully!")

if __name__ == "__main__":
    verify()
