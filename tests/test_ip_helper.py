import unittest
from unittest.mock import patch, MagicMock
from bank_node.utils.ip_helper import is_local_ip
from bank_node.core.config_manager import ConfigManager

class TestIpHelper(unittest.TestCase):
    
    def setUp(self):
        # Reset ConfigManager singleton if needed, though patching is better
        pass
        
    @patch('bank_node.utils.ip_helper.ConfigManager')
    def test_is_local_ip_match_config(self, mock_config_cls):
        # Setup mock config
        mock_instance = MagicMock()
        mock_instance.get.return_value = {"ip": "192.168.1.100", "port": 65525}
        mock_config_cls.return_value = mock_instance
        
        self.assertTrue(is_local_ip("192.168.1.100"))
        self.assertFalse(is_local_ip("192.168.1.101"))

    @patch('bank_node.utils.ip_helper.ConfigManager')
    def test_is_local_ip_localhost_alias(self, mock_config_cls):
        # Setup mock config with 127.0.0.1
        mock_instance = MagicMock()
        mock_instance.get.return_value = {"ip": "127.0.0.1", "port": 65525}
        mock_config_cls.return_value = mock_instance
        
        # Should match both "127.0.0.1" and "localhost"
        self.assertTrue(is_local_ip("127.0.0.1"))
        self.assertTrue(is_local_ip("localhost"))
        self.assertTrue(is_local_ip("LocalHost")) # Case insensitive check

    @patch('bank_node.utils.ip_helper.ConfigManager')
    def test_is_local_ip_config_localhost(self, mock_config_cls):
        # Setup mock config with "localhost"
        mock_instance = MagicMock()
        mock_instance.get.return_value = {"ip": "localhost", "port": 65525}
        mock_config_cls.return_value = mock_instance
        
        # Should match both "127.0.0.1" and "localhost"
        self.assertTrue(is_local_ip("127.0.0.1"))
        self.assertTrue(is_local_ip("localhost"))

    @patch('bank_node.utils.ip_helper.ConfigManager')
    def test_is_local_ip_none_empty(self, mock_config_cls):
        # Setup mock config
        mock_instance = MagicMock()
        mock_instance.get.return_value = {"ip": "127.0.0.1"}
        mock_config_cls.return_value = mock_instance
        
        self.assertFalse(is_local_ip(None))
        self.assertFalse(is_local_ip(""))

if __name__ == '__main__':
    unittest.main()
