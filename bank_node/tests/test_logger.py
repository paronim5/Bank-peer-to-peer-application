import unittest
import os
import sys
import logging

# Ensure core and utils can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import Logger
from core.config_manager import ConfigManager

class TestLogger(unittest.TestCase):
    def setUp(self):
        # Reset ConfigManager and Logger for clean state if possible, 
        # but Singleton makes it hard. We will just test functionality.
        pass

    def test_singleton(self):
        """Verify that Logger follows the Singleton pattern."""
        l1 = Logger()
        l2 = Logger()
        self.assertIs(l1, l2, "Logger instances are not the same (Singleton failed)")

    def test_log_creation(self):
        """Verify that logging creates a file and writes to it."""
        logger = Logger()
        msg = "Test log message"
        logger.info(msg)
        
        # Get log file path from config
        config = ConfigManager()
        log_file = config.get("logging", {}).get("file", "bank_node.log")
        
        self.assertTrue(os.path.exists(log_file), f"Log file {log_file} was not created")
        
        with open(log_file, 'r') as f:
            content = f.read()
            self.assertIn(msg, content, "Log message not found in log file")

if __name__ == '__main__':
    unittest.main()
