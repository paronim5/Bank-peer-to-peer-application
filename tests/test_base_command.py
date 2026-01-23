import unittest
from unittest.mock import MagicMock
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.core.bank import Bank

class ConcreteCommand(BaseCommand):
    def validate_args(self) -> None:
        if not self.args:
            raise ValueError("No arguments provided")
        if self.args[0] == "fail":
            raise ValueError("Validation failed")
        if self.args[0] == "error":
            raise RuntimeError("Unexpected error")

    def execute_logic(self) -> str:
        return f"SUCCESS {self.args[0]}"

class TestBaseCommand(unittest.TestCase):
    def setUp(self):
        self.mock_bank = MagicMock(spec=Bank)

    def test_execute_success(self):
        cmd = ConcreteCommand(self.mock_bank, ["test"])
        result = cmd.execute()
        self.assertEqual(result, "SUCCESS test")

    def test_execute_validation_error(self):
        cmd = ConcreteCommand(self.mock_bank, ["fail"])
        result = cmd.execute()
        self.assertEqual(result, "ERR Validation failed")

    def test_execute_internal_error(self):
        cmd = ConcreteCommand(self.mock_bank, ["error"])
        result = cmd.execute()
        self.assertEqual(result, "ERR Internal error")
        
    def test_instantiation_error(self):
        # Ensure abstract class cannot be instantiated
        with self.assertRaises(TypeError):
            BaseCommand(self.mock_bank, [])

if __name__ == '__main__':
    unittest.main()
