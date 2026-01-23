import unittest
from unittest.mock import MagicMock, patch
import socket
import threading
import time
from bank_node.network.tcp_server import TcpServer

class TestTcpServer(unittest.TestCase):
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = 9999
        self.server = TcpServer(self.host, self.port)

    def test_init(self):
        self.assertEqual(self.server.host, self.host)
        self.assertEqual(self.server.port, self.port)
        self.assertEqual(self.server.handlers, [])

    @patch('bank_node.network.tcp_server.socket.socket')
    @patch('bank_node.network.tcp_server.ClientHandler')
    def test_start_accepts_client(self, MockClientHandler, MockSocket):
        # Setup mocks
        mock_server_socket = MagicMock()
        MockSocket.return_value = mock_server_socket
        
        # Mock accept to return one client then raise OSError to break loop
        mock_client_socket = MagicMock()
        mock_address = ('127.0.0.1', 12345)
        
        # We need to control the loop in start(). 
        # First accept returns client, second raises exception to stop loop
        mock_server_socket.accept.side_effect = [
            (mock_client_socket, mock_address),
            OSError("Stop loop")
        ]
        
        mock_handler_instance = MockClientHandler.return_value

        # Run start in a separate thread because it blocks
        server_thread = threading.Thread(target=self.server.start)
        server_thread.start()
        
        # Give it a moment to process
        time.sleep(0.1)
        
        # Verify
        mock_server_socket.bind.assert_called_with((self.host, self.port))
        mock_server_socket.listen.assert_called_with(5)
        
        # Check if ClientHandler was created and started
        MockClientHandler.assert_called_with(mock_client_socket, mock_address)
        mock_handler_instance.start.assert_called_once()
        
        # We cannot reliably check self.server.handlers here because the server thread 
        # might have already hit the OSError, triggered finally block, and called stop(),
        # which clears the handlers list.
        # self.assertIn(mock_handler_instance, self.server.handlers)
        
        # Stop server to clean up thread (if it's not already stopped)
        self.server.stop()
        server_thread.join(timeout=1.0)

    @patch('bank_node.network.tcp_server.socket.socket')
    def test_stop(self, MockSocket):
        mock_server_socket = MagicMock()
        MockSocket.return_value = mock_server_socket
        
        # Initialize socket manually as if start() was called
        self.server.server_socket = mock_server_socket
        self.server.is_running = True
        
        # Add a mock handler
        mock_handler = MagicMock()
        mock_handler.is_alive.return_value = True
        self.server.handlers.append(mock_handler)
        
        self.server.stop()
        
        # Verify server socket closed
        mock_server_socket.close.assert_called_once()
        self.assertFalse(self.server.is_running)
        self.assertIsNone(self.server.server_socket)
        
        # Verify handler stopped
        self.assertEqual(mock_handler.running, False)
        mock_handler.client_socket.close.assert_called_once()
        mock_handler.join.assert_called()
        self.assertEqual(self.server.handlers, [])

if __name__ == '__main__':
    unittest.main()
