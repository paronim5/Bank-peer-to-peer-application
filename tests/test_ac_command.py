import unittest
from unittest.mock import MagicMock
from bank_node.protocol.commands.ac_command import ACCommand
from bank_node.core.bank import Bank

class TestACCommand(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)
        self.mock_config_manager = MagicMock()
        self.mock_bank.config_manager = self.mock_config_manager

    def test_execute_logic_creates_account_and_returns_format(self):
        # Setup mock return values
        self.mock_bank.create_account.return_value = 12345
        self.mock_config_manager.get.return_value = {"ip": "10.0.0.1", "port": 65525}
        
        command = ACCommand(self.mock_bank, [])
        result = command.execute_logic()
        
        # Verify bank interaction
        self.mock_bank.create_account.assert_called_once()
        
        # Verify result format
        self.assertEqual(result, "AC 12345/10.0.0.1")

    def test_execute_logic_default_ip_on_missing_config(self):
        self.mock_bank.create_account.return_value = 67890
        self.mock_config_manager.get.return_value = {}
        
        command = ACCommand(self.mock_bank, [])
        result = command.execute_logic()
        
        self.assertEqual(result, "AC 67890/127.0.0.1")

    def test_validate_args_ignores_args(self):
        # Should not raise exception
        command = ACCommand(self.mock_bank, ["extra", "args"])
        try:
            command.validate_args()
        except Exception as e:
            self.fail(f"validate_args raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main()
