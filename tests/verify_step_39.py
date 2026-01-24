import socket
import threading
import time
import unittest
from bank_node.network.proxy_client import ProxyClient

class HangingServer(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', port))
        self.sock.listen(1)
        self.running = True

    def run(self):
        while self.running:
            try:
                self.sock.settimeout(1.0)
                client, _ = self.sock.accept()
                # Hang: Do not send anything, just sleep
                time.sleep(10) 
                client.close()
            except socket.timeout:
                continue
            except Exception:
                break
    
    def stop(self):
        self.running = False
        self.sock.close()

class TestTimeouts(unittest.TestCase):
    def test_proxy_client_timeout(self):
        port = 65530
        server = HangingServer(port)
        server.start()
        time.sleep(0.5) # Allow server to start

        try:
            client = ProxyClient()
            start_time = time.time()
            # This should timeout after 5 seconds (default)
            response = client.send_command('127.0.0.1', port, 'BC')
            duration = time.time() - start_time
            
            print(f"Response: {response}, Duration: {duration:.2f}s")
            
            self.assertEqual(response, "ER Timeout")
            self.assertTrue(4.5 < duration < 6.0, f"Timeout should be approx 5s, got {duration}")
            
        finally:
            server.stop()
            server.join()

if __name__ == "__main__":
    unittest.main()
