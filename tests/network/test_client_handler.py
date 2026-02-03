import unittest
from unittest.mock import MagicMock, patch
import socket
from bank_node.network.client_handler import ClientHandler

class TestClientHandler(unittest.TestCase):
    def setUp(self):
        self.mock_socket = MagicMock(spec=socket.socket)
        self.address = ('127.0.0.1', 12345)
        self.handler = ClientHandler(self.mock_socket, self.address)
        # Prevent run loop from running forever in tests if not mocked correctly
        self.handler.running = False 

    @patch('bank_node.network.client_handler.CommandParser')
    @patch('bank_node.network.client_handler.CommandFactory')
    def test_process_message_valid(self, mock_factory, mock_parser):
        # Setup
        mock_parser.parse.return_value = ('BC', [])
        mock_command = MagicMock()
        mock_command.execute.return_value = "BC 127.0.0.1"
        mock_factory_instance = mock_factory.return_value
        mock_factory_instance.get_command.return_value = mock_command
        
        # Inject the mock factory into the handler (since it's created in __init__)
        self.handler.factory = mock_factory_instance

        # Execute
        response = self.handler._process_message("BC")
        
        # Verify
        self.assertEqual(response, "BC 127.0.0.1")
        mock_parser.parse.assert_called_with("BC")
        mock_factory_instance.get_command.assert_called_with('BC', [])
        mock_command.execute.assert_called_once()

    def test_run_loop(self):
        # Setup mocks for run loop
        self.handler.running = True
        
        # Simulate socket receiving data: "BC\n" then empty (disconnect)
        self.mock_socket.recv.side_effect = [b"BC\n", b""]
        
        # Mock internal processing
        with patch.object(self.handler, '_process_message', return_value="BC 127.0.0.1") as mock_process:
            self.handler.run()
            
            # Verify
            self.mock_socket.recv.assert_called()
            mock_process.assert_called_with("BC")
            self.mock_socket.sendall.assert_called_with(b"BC 127.0.0.1\r\n")
            self.mock_socket.close.assert_called_once()

    def test_buffer_handling(self):
        self.handler.running = True
        # Split message across two recv calls
        self.mock_socket.recv.side_effect = [b"B", b"C\n", b""]
        
        with patch.object(self.handler, '_process_message', return_value="OK") as mock_process:
            self.handler.run()
            
            mock_process.assert_called_with("BC")
            self.mock_socket.sendall.assert_called_with(b"OK\r\n")

    def test_windows_line_endings(self):
        self.handler.running = True
        # Message with \r\n
        self.mock_socket.recv.side_effect = [b"BC\r\n", b""]
        
        with patch.object(self.handler, '_process_message', return_value="OK") as mock_process:
            self.handler.run()
            
            mock_process.assert_called_with("BC")
            self.mock_socket.sendall.assert_called_with(b"OK\r\n")

    def test_telnet_backspace_handling(self):
        self.handler.running = True
        # Simulate typing "AD", then Backspace, then "C" -> "AC"
        # \x08 is Backspace
        self.mock_socket.recv.side_effect = [b"AD\x08C\n", b""]
        
        with patch.object(self.handler, '_process_message', return_value="OK") as mock_process:
            self.handler.run()
            
            mock_process.assert_called_with("AC")
            self.mock_socket.sendall.assert_called_with(b"OK\r\n")

    def test_telnet_delete_handling(self):
        self.handler.running = True
        # Simulate typing "AD", then Delete (0x7f), then "C" -> "AC"
        self.mock_socket.recv.side_effect = [b"AD\x7fC\n", b""]
        
        with patch.object(self.handler, '_process_message', return_value="OK") as mock_process:
            self.handler.run()
            
            mock_process.assert_called_with("AC")
            self.mock_socket.sendall.assert_called_with(b"OK\r\n")

    def test_ansi_stripping(self):
        self.handler.running = True
        # Simulate typing "A", then Left Arrow (\x1b[D), then "B" -> "AB" (ignoring the arrow)
        self.mock_socket.recv.side_effect = [b"A\x1b[DB\n", b""]
        
        with patch.object(self.handler, '_process_message', return_value="OK") as mock_process:
            self.handler.run()
            
            mock_process.assert_called_with("AB")
            self.mock_socket.sendall.assert_called_with(b"OK\r\n")

if __name__ == '__main__':
    unittest.main()
