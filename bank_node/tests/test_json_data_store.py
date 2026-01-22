import unittest
import os
import json
from bank_node.persistence.json_data_store import JsonDataStore

class TestJsonDataStore(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_data.json"
        self.store = JsonDataStore(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            try:
                os.remove(self.test_file)
            except PermissionError:
                pass

    def test_save_and_load(self):
        """Test saving data and loading it back."""
        data = {"test": 123, "nested": {"a": 1}}
        self.store.save_data(data)
        
        loaded = self.store.load_data()
        self.assertEqual(data, loaded)

    def test_load_non_existent(self):
        """Test loading from a file that does not exist."""
        # Ensure file doesn't exist
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            
        loaded = self.store.load_data()
        self.assertEqual(loaded, {})

    def test_load_corrupt(self):
        """Test loading from a corrupt JSON file."""
        with open(self.test_file, 'w') as f:
            f.write("{invalid_json")
        
        loaded = self.store.load_data()
        self.assertEqual(loaded, {})

    def test_save_creates_file(self):
        """Test that saving data actually creates the file."""
        data = {"foo": "bar"}
        self.store.save_data(data)
        self.assertTrue(os.path.exists(self.test_file))

if __name__ == '__main__':
    unittest.main()
