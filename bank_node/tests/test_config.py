import unittest
import os
import json
import sys

# Ensure core can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.config_manager = ConfigManager()

    def test_singleton(self):
        """Verify that ConfigManager follows the Singleton pattern."""
        cm1 = ConfigManager()
        cm2 = ConfigManager()
        self.assertIs(cm1, cm2, "ConfigManager instances are not the same (Singleton failed)")

    def test_load_config(self):
        """Verify that values from a JSON file are correctly loaded."""
        test_data = {
            "test_key": "test_value",
            "server": {"ip": "10.0.0.1", "port": 8080}
        }
        test_file = 'test_config.json'
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        try:
            self.config_manager.load_config(test_file)
            self.assertEqual(self.config_manager.get('test_key'), "test_value")
            self.assertEqual(self.config_manager.get('server')['ip'], "10.0.0.1")
            self.assertEqual(self.config_manager.get('server')['port'], 8080)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_defaults_on_missing_file(self):
        """Verify that defaults are loaded when config file is missing."""
        missing_file = 'non_existent_config.json'
        if os.path.exists(missing_file):
            os.remove(missing_file)
            
        self.config_manager.load_config(missing_file)
        
        # Check for default values
        server_config = self.config_manager.get('server')
        self.assertIsNotNone(server_config)
        self.assertEqual(server_config.get('ip'), "127.0.0.1")
        self.assertEqual(server_config.get('port'), 65525)

if __name__ == '__main__':
    unittest.main()
