import unittest
from unittest.mock import MagicMock, patch
from bank_node.protocol.commands.rp_command import RPCommand
from robbery.bank_info import BankInfo
from bank_node.core.bank import Bank

class TestRPCommand(unittest.TestCase):
    def setUp(self):
        self.bank = MagicMock(spec=Bank)
        self.command = RPCommand(self.bank, ["1000"])

    def test_validate_args_valid(self):
        self.assertTrue(self.command.validate_args())

    def test_validate_args_invalid(self):
        cmd = RPCommand(self.bank, [])
        self.assertFalse(cmd.validate_args())
        
        cmd = RPCommand(self.bank, ["abc"])
        self.assertFalse(cmd.validate_args())
        
        cmd = RPCommand(self.bank, ["-100"])
        self.assertFalse(cmd.validate_args())

    @patch('bank_node.protocol.commands.rp_command.NetworkScanner')
    @patch('bank_node.protocol.commands.rp_command.ConfigManager')
    def test_execute_logic_success(self, mock_config_cls, mock_scanner_cls):
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_cls.return_value = mock_config_instance
        # Use default DP strategy
        mock_config_instance.get.side_effect = lambda key, default=None: default
        
        mock_scanner_instance = MagicMock()
        mock_scanner_cls.return_value = mock_scanner_instance
        
        # Mock scan results
        # Bank A: 500, 5 clients
        # Bank B: 500, 5 clients
        # Total 1000, 10 clients
        banks = [
            BankInfo("192.168.1.10", 500, 5),
            BankInfo("192.168.1.11", 500, 5)
        ]
        mock_scanner_instance.scan.return_value = banks
        
        # Execute
        result = self.command.execute()
        
        # Verify
        self.assertIn("RP To achieve 1000", result)
        self.assertIn("rob banks 192.168.1.10 and 192.168.1.11", result)
        self.assertIn("affecting 10 clients", result)

    @patch('bank_node.protocol.commands.rp_command.NetworkScanner')
    @patch('bank_node.protocol.commands.rp_command.ConfigManager')
    def test_execute_logic_single_bank(self, mock_config_cls, mock_scanner_cls):
        mock_config_instance = MagicMock()
        mock_config_cls.return_value = mock_config_instance
        mock_scanner_instance = MagicMock()
        mock_scanner_cls.return_value = mock_scanner_instance
        
        banks = [BankInfo("192.168.1.10", 1000, 5)]
        mock_scanner_instance.scan.return_value = banks
        
        result = self.command.execute()
        
        self.assertIn("rob bank 192.168.1.10", result)
        self.assertIn("affecting 5 clients", result)

    @patch('bank_node.protocol.commands.rp_command.NetworkScanner')
    @patch('bank_node.protocol.commands.rp_command.ConfigManager')
    def test_execute_logic_no_plan(self, mock_config_cls, mock_scanner_cls):
        mock_config_instance = MagicMock()
        mock_config_cls.return_value = mock_config_instance
        mock_scanner_instance = MagicMock()
        mock_scanner_cls.return_value = mock_scanner_instance
        
        # No banks found
        mock_scanner_instance.scan.return_value = []
        
        result = self.command.execute()
        
        self.assertIn("no plan could be formed", result)

if __name__ == '__main__':
    unittest.main()
