import unittest
from bank_node.core.bank import Bank
from bank_node.core.account_repository import AccountRepository
from bank_node.persistence.i_data_store import IDataStore
from bank_node.core.bank_account import BankAccount

class MockDataStore(IDataStore):
    def __init__(self):
        self.data = {}
    def save_data(self, data):
        self.data = data
    def load_data(self):
        return self.data

class TestBank(unittest.TestCase):
    def setUp(self):
        # Reset Singleton for testing
        Bank._instance = None
        self.mock_store = MockDataStore()
        self.repo = AccountRepository(self.mock_store)
        self.bank = Bank(self.repo)

    def test_singleton(self):
        bank2 = Bank()
        self.assertIs(self.bank, bank2)

    def test_create_account(self):
        account_number = self.bank.create_account()
        self.assertTrue(10000 <= account_number <= 99999)
        self.assertIsNotNone(self.repo.get_account(account_number))

    def test_deposit_withdraw(self):
        account_number = self.bank.create_account()
        
        # Deposit
        new_balance = self.bank.deposit(account_number, 500)
        self.assertEqual(new_balance, 500)
        self.assertEqual(self.bank.get_balance(account_number), 500)
        
        # Withdraw
        new_balance = self.bank.withdraw(account_number, 200)
        self.assertEqual(new_balance, 300)
        self.assertEqual(self.bank.get_balance(account_number), 300)

    def test_withdraw_insufficient_funds(self):
        account_number = self.bank.create_account()
        with self.assertRaises(ValueError):
            self.bank.withdraw(account_number, 100)

    def test_get_total_capital(self):
        acc1 = self.bank.create_account()
        acc2 = self.bank.create_account()
        
        self.bank.deposit(acc1, 1000)
        self.bank.deposit(acc2, 2000)
        
        self.assertEqual(self.bank.get_total_capital(), 3000)

    def test_get_client_count(self):
        self.assertEqual(self.bank.get_client_count(), 0)
        self.bank.create_account()
        self.assertEqual(self.bank.get_client_count(), 1)
        self.bank.create_account()
        self.assertEqual(self.bank.get_client_count(), 2)

if __name__ == '__main__':
    unittest.main()
