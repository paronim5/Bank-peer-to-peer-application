import unittest
from bank_node.persistence.i_data_store import IDataStore

class TestIDataStore(unittest.TestCase):
    def test_cannot_instantiate_interface(self):
        """Test that the abstract base class cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            IDataStore()

    def test_concrete_implementation(self):
        """Test that a concrete class implementing all abstract methods works."""
        class MockDataStore(IDataStore):
            def save_data(self, data):
                pass
            def load_data(self):
                return {}
        
        store = MockDataStore()
        self.assertIsInstance(store, IDataStore)

    def test_incomplete_implementation(self):
        """Test that a concrete class missing abstract methods cannot be instantiated."""
        class IncompleteDataStore(IDataStore):
            def save_data(self, data):
                pass
            # Missing load_data
        
        with self.assertRaises(TypeError):
            IncompleteDataStore()

if __name__ == '__main__':
    unittest.main()
