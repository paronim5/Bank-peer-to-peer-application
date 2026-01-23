import unittest
from unittest.mock import MagicMock
from bank_node.protocol.commands.ab_command import ABCommand
from bank_node.core.bank import Bank

class TestABCommand(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)

    def test_validate_args_valid(self):
        """Test valid arguments."""
        cmd = ABCommand(self.mock_bank, ["10000/127.0.0.1"])
        cmd.validate_args()

    def test_validate_args_invalid_count(self):
        """Test invalid argument count."""
        cmd = ABCommand(self.mock_bank, ["10000/127.0.0.1", "extra"])
        with self.assertRaises(ValueError):
            cmd.validate_args()

    def test_execute_logic(self):
        """Test balance retrieval."""
        cmd = ABCommand(self.mock_bank, ["10000/127.0.0.1"])
        self.mock_bank.get_balance.return_value = 500
        
        result = cmd.execute()
        self.assertEqual(result, "AB 500")
        self.mock_bank.get_balance.assert_called_with(10000)

if __name__ == '__main__':
    unittest.main()
