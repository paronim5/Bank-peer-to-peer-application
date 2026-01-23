import unittest
from unittest.mock import patch, MagicMock
import socket
from bank_node.network.proxy_client import ProxyClient

class TestProxyClient(unittest.TestCase):
    def setUp(self):
        self.proxy = ProxyClient()

    @patch('socket.socket')
    def test_send_command_success(self, mock_socket_cls):
        # Setup mock socket
        mock_socket = MagicMock()
        mock_socket_cls.return_value.__enter__.return_value = mock_socket
        
        # Setup response
        mock_socket.recv.return_value = b"OK Success"
        
        response = self.proxy.send_command("127.0.0.1", 65525, "TEST\n")
        
        # Verify interactions
        mock_socket.connect.assert_called_with(("127.0.0.1", 65525))
        mock_socket.settimeout.assert_called_with(5.0)
        mock_socket.sendall.assert_called_with(b"TEST\n")
        self.assertEqual(response, "OK Success")

    @patch('socket.socket')
    def test_send_command_timeout(self, mock_socket_cls):
        # Setup mock socket to raise timeout on connect
        mock_socket = MagicMock()
        mock_socket_cls.return_value.__enter__.return_value = mock_socket
        mock_socket.connect.side_effect = socket.timeout
        
        response = self.proxy.send_command("127.0.0.1", 65525, "TEST")
        
        self.assertEqual(response, "ER Timeout")

    @patch('socket.socket')
    def test_send_command_connection_refused(self, mock_socket_cls):
        # Setup mock socket to raise ConnectionRefusedError
        mock_socket = MagicMock()
        mock_socket_cls.return_value.__enter__.return_value = mock_socket
        mock_socket.connect.side_effect = ConnectionRefusedError
        
        response = self.proxy.send_command("127.0.0.1", 65525, "TEST")
        
        self.assertEqual(response, "ER Connection failed")

    @patch('socket.socket')
    def test_send_command_generic_error(self, mock_socket_cls):
        # Setup mock socket to raise generic Exception
        mock_socket = MagicMock()
        mock_socket_cls.return_value.__enter__.return_value = mock_socket
        mock_socket.connect.side_effect = Exception("Unknown error")
        
        response = self.proxy.send_command("127.0.0.1", 65525, "TEST")
        
        self.assertEqual(response, "ER Unknown error")

if __name__ == '__main__':
    unittest.main()
