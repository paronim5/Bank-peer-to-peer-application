import unittest
from unittest.mock import MagicMock, patch
from bank_node.protocol.commands.bc_command import BCCommand
from bank_node.core.bank import Bank

class TestBCCommand(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)
        self.mock_config_manager = MagicMock()
        self.mock_bank.config_manager = self.mock_config_manager

    def test_execute_logic_returns_ip(self):
        self.mock_config_manager.get.return_value = {"ip": "192.168.1.100", "port": 65525}
        
        command = BCCommand(self.mock_bank, [])
        result = command.execute_logic()
        
        self.assertEqual(result, "BC 192.168.1.100")
        self.mock_config_manager.get.assert_called_with("server")

    def test_execute_logic_default_ip_on_missing_config(self):
        self.mock_config_manager.get.return_value = {}
        
        command = BCCommand(self.mock_bank, [])
        result = command.execute_logic()
        
        self.assertEqual(result, "BC 127.0.0.1")

    @patch("bank_node.protocol.commands.bc_command.get_primary_local_ip")
    def test_execute_logic_uses_primary_ip_when_bound_all_interfaces(self, mock_get_ip):
        self.mock_config_manager.get.return_value = {"ip": "0.0.0.0", "port": 65525}
        mock_get_ip.return_value = "10.0.0.123"

        command = BCCommand(self.mock_bank, [])
        result = command.execute_logic()

        self.assertEqual(result, "BC 10.0.0.123")
        mock_get_ip.assert_called_once()
        
    def test_validate_args_ignores_args(self):
        command = BCCommand(self.mock_bank, ["arg1", "arg2"])
        try:
            command.validate_args()
        except Exception as e:
            self.fail(f"validate_args raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main()
