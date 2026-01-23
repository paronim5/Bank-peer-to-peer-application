import unittest
from bank_node.protocol.command_parser import CommandParser
from bank_node.protocol.command_enum import CommandType

class TestCommandParser(unittest.TestCase):
    def test_parse_valid_command_with_args(self):
        raw_data = "AD 10001/10.1.2.3 500"
        command, args = CommandParser.parse(raw_data)
        self.assertEqual(command, "AD")
        self.assertEqual(args, ["10001/10.1.2.3", "500"])

    def test_parse_valid_command_no_args(self):
        raw_data = "BC"
        command, args = CommandParser.parse(raw_data)
        self.assertEqual(command, "BC")
        self.assertEqual(args, [])

    def test_parse_valid_command_extra_whitespace(self):
        raw_data = "  AD   10001/10.1.2.3    500  \n"
        command, args = CommandParser.parse(raw_data)
        self.assertEqual(command, "AD")
        self.assertEqual(args, ["10001/10.1.2.3", "500"])

    def test_parse_invalid_command_code(self):
        raw_data = "INVALID 123"
        command, args = CommandParser.parse(raw_data)
        self.assertIsNone(command)
        self.assertEqual(args, [])

    def test_parse_empty_string(self):
        raw_data = ""
        command, args = CommandParser.parse(raw_data)
        self.assertIsNone(command)
        self.assertEqual(args, [])

    def test_parse_whitespace_only(self):
        raw_data = "   \n  "
        command, args = CommandParser.parse(raw_data)
        self.assertIsNone(command)
        self.assertEqual(args, [])

    def test_parse_none(self):
        raw_data = None
        # The type hint says str, but good to handle None if possible or just rely on static typing
        # Our implementation handles "if not raw_data" which covers None
        command, args = CommandParser.parse(raw_data)
        self.assertIsNone(command)
        self.assertEqual(args, [])

if __name__ == '__main__':
    unittest.main()
