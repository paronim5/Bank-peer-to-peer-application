import unittest
from bank_node.core.account_repository import AccountRepository
from bank_node.core.bank_account import BankAccount
from bank_node.persistence.i_data_store import IDataStore

class MockDataStore(IDataStore):
    def __init__(self):
        self.data = {}

    def save_data(self, data: dict):
        self.data = data

    def load_data(self) -> dict:
        return self.data

class TestAccountRepository(unittest.TestCase):
    def setUp(self):
        self.mock_store = MockDataStore()
        self.repo = AccountRepository(self.mock_store)

    def test_add_and_get_account(self):
        acc = BankAccount(10123, 1000)
        self.repo.add_account(acc)
        
        retrieved = self.repo.get_account(10123)
        self.assertEqual(retrieved, acc)
        self.assertEqual(retrieved.balance, 1000)

    def test_get_non_existent_account(self):
        self.assertIsNone(self.repo.get_account(99999))

    def test_remove_account(self):
        acc = BankAccount(10456, 500)
        self.repo.add_account(acc)
        self.repo.remove_account(10456)
        self.assertIsNone(self.repo.get_account(10456))

    def test_get_all_accounts(self):
        acc1 = BankAccount(10001, 100)
        acc2 = BankAccount(10002, 200)
        self.repo.add_account(acc1)
        self.repo.add_account(acc2)
        
        all_accounts = self.repo.get_all_accounts()
        self.assertEqual(len(all_accounts), 2)
        self.assertIn(acc1, all_accounts)
        self.assertIn(acc2, all_accounts)

    def test_save_and_load(self):
        # Create repo with some data
        acc = BankAccount(10789, 5000)
        self.repo.add_account(acc)
        
        # Save to mock store
        self.repo.save()
        
        # Verify store has data
        stored_data = self.mock_store.data
        self.assertIn("10789", stored_data)
        self.assertEqual(stored_data["10789"]["balance"], 5000)
        
        # Create new repo with same store (simulate restart)
        new_repo = AccountRepository(self.mock_store)
        new_repo.load()
        
        # Verify data loaded back
        loaded_acc = new_repo.get_account(10789)
        self.assertIsNotNone(loaded_acc)
        self.assertEqual(loaded_acc.number, 10789)
        self.assertEqual(loaded_acc.balance, 5000)

if __name__ == '__main__':
    unittest.main()
