import threading
import unittest
import os
import shutil
from bank_node.core.bank import Bank
from bank_node.core.account_repository import AccountRepository
from bank_node.persistence.json_data_store import JsonDataStore

class TestBankThreadSafety(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.getcwd(), "tests", "temp_data")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        
        self.db_path = os.path.join(self.test_dir, "bank_data.json")
        self.data_store = JsonDataStore(self.db_path)
        self.repo = AccountRepository(self.data_store)
        
        # Reset Bank singleton
        Bank._instance = None
        self.bank = Bank(self.repo)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        Bank._instance = None

    def test_concurrent_account_creation(self):
        """Test creating accounts from multiple threads simultaneously."""
        num_threads = 50
        accounts = []
        errors = []
        lock = threading.Lock()

        def create_worker():
            try:
                acc_num = self.bank.create_account()
                with lock:
                    accounts.append(acc_num)
            except Exception as e:
                with lock:
                    errors.append(e)

        threads = [threading.Thread(target=create_worker) for _ in range(num_threads)]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()

        if errors:
            print(f"Errors encountered: {errors}")

        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
        self.assertEqual(self.bank.get_client_count(), num_threads)
        self.assertEqual(len(set(accounts)), num_threads, "Duplicate account numbers found")

    def test_concurrent_deposits(self):
        """Test depositing to the same account from multiple threads."""
        acc_num = self.bank.create_account()
        num_threads = 50
        deposit_amount = 10
        errors = []
        lock = threading.Lock()
        
        def deposit_worker():
            try:
                self.bank.deposit(acc_num, deposit_amount)
            except Exception as e:
                with lock:
                    errors.append(e)

        threads = [threading.Thread(target=deposit_worker) for _ in range(num_threads)]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()

        if errors:
            print(f"Deposit errors: {errors}")

        expected_balance = num_threads * deposit_amount
        self.assertEqual(self.bank.get_balance(acc_num), expected_balance)

if __name__ == '__main__':
    unittest.main()
