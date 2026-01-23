import unittest
from unittest.mock import MagicMock
from bank_node.protocol.commands.ba_command import BACommand
from bank_node.core.bank import Bank

class TestBACommand(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)

    def test_execute_success(self):
        """Test successful total capital retrieval."""
        self.mock_bank.get_total_capital.return_value = 50000
        cmd = BACommand(self.mock_bank, [])
        
        result = cmd.execute()
        self.assertEqual(result, "BA 50000")
        self.mock_bank.get_total_capital.assert_called_once()

    def test_execute_zero_capital(self):
        """Test retrieval when capital is zero."""
        self.mock_bank.get_total_capital.return_value = 0
        cmd = BACommand(self.mock_bank, [])
        
        result = cmd.execute()
        self.assertEqual(result, "BA 0")

    def test_invalid_args(self):
        """Test validation error with arguments."""
        cmd = BACommand(self.mock_bank, ["arg1"])
        result = cmd.execute()
        self.assertIn("Invalid arguments count", result)

if __name__ == '__main__':
    unittest.main()
