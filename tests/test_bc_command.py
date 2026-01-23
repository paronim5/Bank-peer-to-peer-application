import unittest
from unittest.mock import MagicMock
from bank_node.protocol.commands.bc_command import BCCommand
from bank_node.core.bank import Bank

class TestBCCommand(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)
        self.mock_config_manager = MagicMock()
        self.mock_bank.config_manager = self.mock_config_manager

    def test_execute_logic_returns_ip(self):
        # Setup mock config
        self.mock_config_manager.get.return_value = {"ip": "192.168.1.100", "port": 65525}
        
        command = BCCommand(self.mock_bank, [])
        result = command.execute_logic()
        
        self.assertEqual(result, "BC 192.168.1.100")
        self.mock_config_manager.get.assert_called_with("server")

    def test_execute_logic_default_ip_on_missing_config(self):
        # Setup mock config to return None or empty
        self.mock_config_manager.get.return_value = {}
        
        command = BCCommand(self.mock_bank, [])
        result = command.execute_logic()
        
        self.assertEqual(result, "BC 127.0.0.1")

    def test_validate_args_ignores_args(self):
        # Should not raise exception
        command = BCCommand(self.mock_bank, ["arg1", "arg2"])
        try:
            command.validate_args()
        except Exception as e:
            self.fail(f"validate_args raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main()
