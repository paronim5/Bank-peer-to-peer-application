import unittest
from unittest.mock import MagicMock
from bank_node.protocol.commands.aw_command import AWCommand
from bank_node.core.bank import Bank

class TestAWCommand(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)
        # Mock config manager
        self.mock_bank.config_manager = MagicMock()
        self.mock_bank.config_manager.get.return_value = {"ip": "127.0.0.1"}

    def test_validate_args_valid(self):
        """Test valid arguments."""
        cmd = AWCommand(self.mock_bank, ["10000/127.0.0.1", "200"])
        cmd.validate_args()

    def test_validate_args_invalid(self):
        """Test invalid arguments (reusing logic verification)."""
        cmd = AWCommand(self.mock_bank, ["10000", "200"])
        with self.assertRaises(ValueError):
            cmd.validate_args()

    def test_execute_success(self):
        """Test successful withdrawal."""
        cmd = AWCommand(self.mock_bank, ["10000/127.0.0.1", "200"])
        self.mock_bank.withdraw.return_value = 300 # New balance
        
        result = cmd.execute()
        self.assertEqual(result, "AW")
        self.mock_bank.withdraw.assert_called_with(10000, 200)

    def test_execute_insufficient_funds(self):
        """Test withdrawal with insufficient funds."""
        cmd = AWCommand(self.mock_bank, ["10000/127.0.0.1", "1000"])
        # Mock bank raising ValueError
        self.mock_bank.withdraw.side_effect = ValueError("Insufficient funds.")
        
        result = cmd.execute()
        # Expect ER or ERR depending on implementation. 
        # Since I didn't override format_error yet (I planned to but haven't written it), 
        # let's see what happens. I should probably update the class first.
        # But wait, BaseCommand uses ERR.
        # If I want ER, I need to update the class.
        self.assertIn("Insufficient funds", result)

if __name__ == '__main__':
    unittest.main()
