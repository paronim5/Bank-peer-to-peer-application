import socket
import unittest
import time
import threading
from unittest.mock import patch, MagicMock
from bank_node.network.client_handler import ClientHandler

class TestServerTimeout(unittest.TestCase):
    @patch('bank_node.network.client_handler.ConfigManager')
    def test_client_handler_timeout(self, mock_config_cls):
        # Mock config to return 2.0s timeout
        # structure: config.get("network", {}).get("client_timeout", 60.0)
        mock_config = mock_config_cls.return_value
        
        # We need to handle the chained .get() calls
        # config.get("network", {}) returns a dict-like object (or dict)
        # .get("client_timeout", ...) returns 2.0
        
        # Simpler approach: side_effect
        def get_side_effect(key, default=None):
            if key == "network":
                return {"client_timeout": 2.0}
            return default
        
        mock_config.get.side_effect = get_side_effect
        
        # Create a real server socket to ensure Windows compatibility
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(('127.0.0.1', 0))
        port = listener.getsockname()[1]
        listener.listen(1)
        
        client_thread = None
        server_sock = None
        
        try:
            # Connect from client
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect in a thread or non-blocking to avoid deadlock if accept blocks?
            # accept is blocking, connect is blocking.
            # We need to call accept.
            
            def connect_client():
                client_sock.connect(('127.0.0.1', port))
                
            connect_thread = threading.Thread(target=connect_client)
            connect_thread.start()
            
            server_sock, addr = listener.accept()
            connect_thread.join()
            
            # Now we have server_sock (passed to handler) and client_sock (our test client)
            
            # Start handler
            handler = ClientHandler(server_sock, addr)
            handler.start()
            
            # Wait for timeout (2s + buffer)
            time.sleep(3.0)
            
            # Handler should have closed server_sock upon timeout
            # client_sock.recv should return b'' (EOF)
            try:
                data = client_sock.recv(1024)
                self.assertEqual(data, b'') 
            except ConnectionResetError:
                # Also acceptable
                pass
                
            handler.join(timeout=1)
            self.assertFalse(handler.is_alive())
            
        finally:
            if client_sock: client_sock.close()
            if server_sock: server_sock.close()
            listener.close()

if __name__ == "__main__":
    unittest.main()
