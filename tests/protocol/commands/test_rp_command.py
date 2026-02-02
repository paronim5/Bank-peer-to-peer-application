import unittest
from unittest.mock import MagicMock, patch
from bank_node.protocol.commands.rp_command import RPCommand
from bank_node.robbery.bank_info import BankInfo
from bank_node.core.bank import Bank

class TestRPCommand(unittest.TestCase):
    def setUp(self):
        self.bank = MagicMock(spec=Bank)
        # Mock config manager on bank
        self.bank.config_manager = MagicMock()
        self.command = RPCommand(self.bank, ["1000"])

    def test_validate_args_valid(self):
        # Should not raise exception
        self.command.validate_args()

    def test_validate_args_invalid(self):
        cmd = RPCommand(self.bank, [])
        with self.assertRaises(ValueError):
            cmd.validate_args()
        
        cmd = RPCommand(self.bank, ["abc"])
        with self.assertRaises(ValueError):
            cmd.validate_args()

    @patch('bank_node.protocol.commands.rp_command.NetworkScanner')
    def test_execute_logic_success(self, mock_scanner_cls):
        # Setup mocks
        mock_scanner_instance = MagicMock()
        mock_scanner_cls.return_value = mock_scanner_instance
        
        # Mock scan results
        # Bank A: 500, 5 clients
        # Bank B: 500, 5 clients
        # Total 1000, 10 clients
        banks = [
            BankInfo("192.168.1.10", 65525, 500, 5),
            BankInfo("192.168.1.11", 65525, 500, 5)
        ]
        mock_scanner_instance.scan.return_value = banks
        
        # Execute
        result = self.command.execute()
        
        self.assertIn("RP To achieve 1000", result)
        self.assertIn("rob banks", result)
        self.assertIn("affecting only 10 clients", result)
        self.assertIn("(Total: 1000)", result)

    @patch('bank_node.protocol.commands.rp_command.NetworkScanner')
    def test_execute_logic_single_bank(self, mock_scanner_cls):
        mock_scanner_instance = MagicMock()
        mock_scanner_cls.return_value = mock_scanner_instance
        
        banks = [BankInfo("192.168.1.10", 65525, 1000, 5)]
        mock_scanner_instance.scan.return_value = banks
        
        result = self.command.execute()
        
        self.assertIn("rob banks 192.168.1.10", result)
        self.assertIn("affecting only 5 clients", result)

    @patch('bank_node.protocol.commands.rp_command.NetworkScanner')
    def test_execute_logic_no_banks(self, mock_scanner_cls):
        mock_scanner_instance = MagicMock()
        mock_scanner_cls.return_value = mock_scanner_instance
        
        # No banks found
        mock_scanner_instance.scan.return_value = []
        
        result = self.command.execute()
        
        self.assertIn("RP No banks found to rob", result)

    @patch('bank_node.protocol.commands.rp_command.NetworkScanner')
    def test_execute_logic_no_plan(self, mock_scanner_cls):
        mock_scanner_instance = MagicMock()
        mock_scanner_cls.return_value = mock_scanner_instance
        
        # Bank found but too big for our target (Knapsack 0/1 constraint)
        banks = [BankInfo("192.168.1.10", 65525, 2000, 5)]
        mock_scanner_instance.scan.return_value = banks
        
        # Target is 1000 (from setUp)
        result = self.command.execute()
        
        self.assertIn("no suitable banks found", result)

if __name__ == '__main__':
    unittest.main()
