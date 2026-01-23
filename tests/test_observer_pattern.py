import unittest
import os
import shutil
from bank_node.core.bank import Bank
from bank_node.core.account_repository import AccountRepository
from bank_node.persistence.json_data_store import JsonDataStore
from bank_node.persistence.auto_saver import AutoSaver

class TestObserverPattern(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.getcwd(), "tests", "temp_observer_data")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        
        self.db_path = os.path.join(self.test_dir, "bank_data.json")
        self.data_store = JsonDataStore(self.db_path)
        self.repo = AccountRepository(self.data_store)
        
        # Reset Bank singleton
        Bank._instance = None
        self.bank = Bank(self.repo)
        
        # Initialize AutoSaver and subscribe it
        self.auto_saver = AutoSaver(self.repo)
        self.bank.subscribe(self.auto_saver)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        Bank._instance = None

    def test_auto_save_on_create_account(self):
        """Test that account creation triggers auto-save."""
        # Ensure file doesn't exist initially (or is empty)
        # AccountRepository doesn't create file on init, only on save.
        self.assertFalse(os.path.exists(self.db_path))
        
        acc_num = self.bank.create_account()
        
        # Check if file exists and contains the account
        self.assertTrue(os.path.exists(self.db_path))
        
        # Load data to verify
        loaded_data = self.data_store.load_data()
        self.assertIn(str(acc_num), loaded_data)
        self.assertEqual(loaded_data[str(acc_num)]["balance"], 0)

    def test_auto_save_on_deposit(self):
        """Test that deposit triggers auto-save."""
        acc_num = self.bank.create_account()
        
        # Verify initial state
        loaded_data = self.data_store.load_data()
        self.assertEqual(loaded_data[str(acc_num)]["balance"], 0)
        
        # Perform deposit
        self.bank.deposit(acc_num, 100)
        
        # Verify update in file
        loaded_data = self.data_store.load_data()
        self.assertEqual(loaded_data[str(acc_num)]["balance"], 100)

    def test_auto_save_on_withdraw(self):
        """Test that withdraw triggers auto-save."""
        acc_num = self.bank.create_account()
        self.bank.deposit(acc_num, 100)
        
        # Perform withdraw
        self.bank.withdraw(acc_num, 50)
        
        # Verify update in file
        loaded_data = self.data_store.load_data()
        self.assertEqual(loaded_data[str(acc_num)]["balance"], 50)

    def test_unsubscribe(self):
        """Test that unsubscribing stops auto-save."""
        acc_num = self.bank.create_account()
        
        self.bank.unsubscribe(self.auto_saver)
        
        # Perform deposit (should NOT save to file)
        self.bank.deposit(acc_num, 100)
        
        # Verify file still has old balance
        loaded_data = self.data_store.load_data()
        self.assertEqual(loaded_data[str(acc_num)]["balance"], 0)
        
        # Verify in-memory balance is updated
        self.assertEqual(self.bank.get_balance(acc_num), 100)

if __name__ == '__main__':
    unittest.main()
