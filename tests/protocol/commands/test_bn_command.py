import unittest
from unittest.mock import MagicMock
from bank_node.protocol.commands.bn_command import BNCommand
from bank_node.core.bank import Bank

class TestBNCommand(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)

    def test_execute_success(self):
        """Test successful client count retrieval."""
        self.mock_bank.get_client_count.return_value = 5
        cmd = BNCommand(self.mock_bank, [])
        
        result = cmd.execute()
        self.assertEqual(result, "BN 5")
        self.mock_bank.get_client_count.assert_called_once()

    def test_execute_zero_clients(self):
        """Test retrieval when no clients exist."""
        self.mock_bank.get_client_count.return_value = 0
        cmd = BNCommand(self.mock_bank, [])
        
        result = cmd.execute()
        self.assertEqual(result, "BN 0")

    def test_invalid_args(self):
        """Test validation error with arguments."""
        cmd = BNCommand(self.mock_bank, ["arg1"])
        result = cmd.execute()
        self.assertIn("Invalid arguments count", result)

if __name__ == '__main__':
    unittest.main()
