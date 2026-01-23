import unittest
from unittest.mock import MagicMock
from bank_node.protocol.commands.ar_command import ARCommand
from bank_node.core.bank import Bank

class TestARCommand(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)

    def test_execute_success(self):
        """Test successful account removal."""
        cmd = ARCommand(self.mock_bank, ["10000/127.0.0.1"])
        
        result = cmd.execute()
        self.assertEqual(result, "AR")
        self.mock_bank.remove_account.assert_called_with(10000)

    def test_execute_with_funds(self):
        """Test removal failure due to funds."""
        cmd = ARCommand(self.mock_bank, ["10000/127.0.0.1"])
        self.mock_bank.remove_account.side_effect = ValueError("Cannot delete account with funds.")
        
        result = cmd.execute()
        self.assertIn("Cannot delete account with funds", result)

if __name__ == '__main__':
    unittest.main()
