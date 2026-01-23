import unittest
from bank_node.protocol.command_enum import CommandType

class TestCommandEnum(unittest.TestCase):
    def test_enum_members(self):
        """Verify all expected commands are present."""
        expected_commands = {"BC", "AC", "AD", "AW", "AB", "AR", "BA", "BN", "RP"}
        actual_commands = {member.value for member in CommandType}
        self.assertEqual(expected_commands, actual_commands)

    def test_is_valid(self):
        """Verify the is_valid static method."""
        self.assertTrue(CommandType.is_valid("BC"))
        self.assertTrue(CommandType.is_valid("AC"))
        self.assertTrue(CommandType.is_valid("RP"))
        
        self.assertFalse(CommandType.is_valid("XYZ"))
        self.assertFalse(CommandType.is_valid("bc")) # Case sensitive
        self.assertFalse(CommandType.is_valid(""))

if __name__ == '__main__':
    unittest.main()
