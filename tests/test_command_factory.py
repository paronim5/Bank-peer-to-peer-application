import unittest
from unittest.mock import MagicMock
from bank_node.protocol.command_factory import CommandFactory
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.core.bank import Bank
from bank_node.protocol.command_enum import CommandType

class DummyCommand(BaseCommand):
    def validate_args(self) -> None:
        pass
    def execute_logic(self) -> str:
        return "DUMMY"

class TestCommandFactory(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)
        self.factory = CommandFactory(self.mock_bank)

    def test_get_command_valid_registered(self):
        # Register a dummy command for a valid type (e.g., BC)
        # Note: BC is a valid CommandType member
        self.factory.register_command(CommandType.BC.value, DummyCommand)
        
        cmd = self.factory.get_command("BC", ["arg1"])
        self.assertIsInstance(cmd, DummyCommand)
        self.assertEqual(cmd.args, ["arg1"])
        self.assertEqual(cmd.bank, self.mock_bank)

    def test_get_command_invalid_type(self):
        cmd = self.factory.get_command("INVALID_CMD", [])
        self.assertIsNone(cmd)

    def test_get_command_unregistered_valid_type(self):
        # AC is valid but not registered
        cmd = self.factory.get_command("AC", [])
        self.assertIsNone(cmd)

if __name__ == '__main__':
    unittest.main()
