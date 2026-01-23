import unittest
from bank_node.protocol.validator import Validator

class TestValidator(unittest.TestCase):
    def test_validate_ip(self):
        # Valid IPs
        self.assertTrue(Validator.validate_ip("192.168.1.1"))
        self.assertTrue(Validator.validate_ip("10.0.0.1"))
        self.assertTrue(Validator.validate_ip("127.0.0.1"))
        self.assertTrue(Validator.validate_ip("0.0.0.0"))
        self.assertTrue(Validator.validate_ip("255.255.255.255"))

        # Invalid IPs
        self.assertFalse(Validator.validate_ip("256.256.256.256"))
        self.assertFalse(Validator.validate_ip("192.168.1"))
        self.assertFalse(Validator.validate_ip("192.168.1.1.1"))
        self.assertFalse(Validator.validate_ip("abc.def.ghi.jkl"))
        self.assertFalse(Validator.validate_ip(123))
        self.assertFalse(Validator.validate_ip(""))

    def test_validate_account_number(self):
        # Valid account numbers
        self.assertTrue(Validator.validate_account_number(10000))
        self.assertTrue(Validator.validate_account_number(99999))
        self.assertTrue(Validator.validate_account_number(54321))

        # Invalid account numbers
        self.assertFalse(Validator.validate_account_number(9999))
        self.assertFalse(Validator.validate_account_number(100000))
        self.assertFalse(Validator.validate_account_number("12345"))
        self.assertFalse(Validator.validate_account_number(123.45))

    def test_validate_amount(self):
        # Valid amounts
        self.assertTrue(Validator.validate_amount(0))
        self.assertTrue(Validator.validate_amount(100))
        self.assertTrue(Validator.validate_amount(999999999))

        # Invalid amounts
        self.assertFalse(Validator.validate_amount(-1))
        self.assertFalse(Validator.validate_amount(10.5))
        self.assertFalse(Validator.validate_amount("100"))

    def test_validate_port(self):
        # Valid ports
        self.assertTrue(Validator.validate_port(65525))
        self.assertTrue(Validator.validate_port(65535))
        self.assertTrue(Validator.validate_port(65530))

        # Invalid ports
        self.assertFalse(Validator.validate_port(65524))
        self.assertFalse(Validator.validate_port(65536))
        self.assertFalse(Validator.validate_port(8080))
        self.assertFalse(Validator.validate_port("65530"))

if __name__ == '__main__':
    unittest.main()
