import unittest
import os
import sqlite3
import json
from bank_node.persistence.sqlite_data_store import SqliteDataStore

class TestSqliteDataStore(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_bank.db"
        # Ensure cleanup before start
        if os.path.exists(self.test_file):
            try:
                os.remove(self.test_file)
            except PermissionError:
                pass
        self.store = SqliteDataStore(self.test_file)

    def tearDown(self):
        # Close any lingering connections if possible, though store opens/closes per method
        if os.path.exists(self.test_file):
            try:
                os.remove(self.test_file)
            except PermissionError:
                pass

    def test_save_and_load(self):
        """Test saving data and loading it back."""
        # AccountRepository saves a dict of accounts: {id: {number: id, balance: val}}
        data = {
            "10001": {"number": 10001, "balance": 500, "history": ["tx1"]},
            "10002": {"number": 10002, "balance": 100, "history": []}
        }
        self.store.save_data(data)
        
        loaded = self.store.load_data()
        
        # Verify keys
        self.assertIn("10001", loaded)
        self.assertIn("10002", loaded)
        
        # Verify content
        self.assertEqual(loaded["10001"]["balance"], 500)
        self.assertEqual(loaded["10001"]["history"], ["tx1"])
        self.assertEqual(loaded["10002"]["balance"], 100)
        self.assertEqual(loaded["10002"]["history"], [])

    def test_load_non_existent(self):
        """Test loading when DB file exists but table might be empty or file deleted."""
        # In setUp, store is created which creates the file and table.
        # Let's verify loading empty
        loaded = self.store.load_data()
        self.assertEqual(loaded, {})

    def test_save_creates_file(self):
        """Test that saving data actually creates the file (if not already)."""
        # remove file created by setUp
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            
        data = {"10001": {"number": 10001, "balance": 500}}
        # Note: save_data connects, which creates the file
        self.store.save_data(data)
        self.assertTrue(os.path.exists(self.test_file))

    def test_data_persistence(self):
        """Test that data persists across different store instances."""
        data = {"10001": {"number": 10001, "balance": 999}}
        self.store.save_data(data)
        
        # New instance
        new_store = SqliteDataStore(self.test_file)
        loaded = new_store.load_data()
        self.assertEqual(loaded["10001"]["balance"], 999)

if __name__ == '__main__':
    unittest.main()
