import unittest
from unittest.mock import MagicMock
from bank_node.protocol.commands.ad_command import ADCommand
from bank_node.core.bank import Bank

class TestADCommand(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)
        # Mock config manager
        self.mock_bank.config_manager = MagicMock()
        self.mock_bank.config_manager.get.return_value = {"ip": "127.0.0.1"}

    def test_validate_args_valid(self):
        """Test valid arguments."""
        cmd = ADCommand(self.mock_bank, ["10000/127.0.0.1", "500"])
        # Should not raise exception
        cmd.validate_args()

    def test_validate_args_invalid_count(self):
        """Test invalid argument count."""
        cmd = ADCommand(self.mock_bank, ["10000/127.0.0.1"])
        with self.assertRaises(ValueError):
            cmd.validate_args()

    def test_validate_args_invalid_account_format(self):
        """Test invalid account ID format."""
        cmd = ADCommand(self.mock_bank, ["10000", "500"])
        with self.assertRaises(ValueError):
            cmd.validate_args()

    def test_validate_args_invalid_account_number(self):
        """Test invalid account number (out of range)."""
        cmd = ADCommand(self.mock_bank, ["999/127.0.0.1", "500"])
        with self.assertRaises(ValueError):
            cmd.validate_args()

    def test_validate_args_invalid_ip(self):
        """Test invalid IP address."""
        cmd = ADCommand(self.mock_bank, ["10000/999.999.999.999", "500"])
        with self.assertRaises(ValueError):
            cmd.validate_args()

    def test_validate_args_foreign_ip(self):
        """Test foreign IP (not matching local config)."""
        self.mock_bank.config_manager.get.return_value = {"ip": "192.168.1.1"}
        cmd = ADCommand(self.mock_bank, ["10000/10.0.0.1", "500"])
        with self.assertRaises(ValueError) as cm:
            cmd.validate_args()
        self.assertIn("Foreign account", str(cm.exception))

    def test_validate_args_negative_amount(self):
        """Test negative amount."""
        cmd = ADCommand(self.mock_bank, ["10000/127.0.0.1", "-500"])
        with self.assertRaises(ValueError):
            cmd.validate_args()

    def test_validate_args_non_integer_amount(self):
        """Test non-integer amount."""
        cmd = ADCommand(self.mock_bank, ["10000/127.0.0.1", "abc"])
        with self.assertRaises(ValueError):
            cmd.validate_args()

    def test_execute_logic(self):
        """Test logic execution calls bank.deposit."""
        cmd = ADCommand(self.mock_bank, ["10000/127.0.0.1", "500"])
        result = cmd.execute_logic()
        
        self.assertEqual(result, "AD")
        self.mock_bank.deposit.assert_called_with(10000, 500)

    def test_execute_full_flow(self):
        """Test full execute flow (template method)."""
        cmd = ADCommand(self.mock_bank, ["10000/127.0.0.1", "500"])
        response = cmd.execute()
        self.assertEqual(response, "AD")

if __name__ == '__main__':
    unittest.main()
