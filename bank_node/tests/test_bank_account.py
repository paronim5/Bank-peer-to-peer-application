import unittest
import sys
import os
import threading

# Ensure core can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.bank_account import BankAccount

class TestBankAccount(unittest.TestCase):
    def test_initialization_valid(self):
        acc = BankAccount(10001, 500)
        self.assertEqual(acc.number, 10001)
        self.assertEqual(acc.balance, 500)

    def test_initialization_invalid_number(self):
        with self.assertRaises(ValueError):
            BankAccount(999) # Too small
        with self.assertRaises(ValueError):
            BankAccount(100000) # Too large

    def test_deposit(self):
        acc = BankAccount(10001, 100)
        new_balance = acc.deposit(50)
        self.assertEqual(new_balance, 150)
        self.assertEqual(acc.balance, 150)

    def test_deposit_negative(self):
        acc = BankAccount(10001, 100)
        with self.assertRaises(ValueError):
            acc.deposit(-10)
        self.assertEqual(acc.balance, 100) # Unchanged

    def test_withdraw_success(self):
        acc = BankAccount(10001, 100)
        new_balance = acc.withdraw(40)
        self.assertEqual(new_balance, 60)
        self.assertEqual(acc.balance, 60)

    def test_withdraw_insufficient(self):
        acc = BankAccount(10001, 100)
        with self.assertRaises(ValueError):
            acc.withdraw(150)
        self.assertEqual(acc.balance, 100) # Unchanged

    def test_withdraw_negative(self):
        acc = BankAccount(10001, 100)
        with self.assertRaises(ValueError):
            acc.withdraw(-10)

    def test_serialization(self):
        acc = BankAccount(10001, 200)
        data = acc.to_dict()
        self.assertEqual(data, {"number": 10001, "balance": 200})
        
        acc2 = BankAccount.from_dict(data)
        self.assertEqual(acc2.number, 10001)
        self.assertEqual(acc2.balance, 200)

    def test_thread_safety(self):
        """Test that concurrent deposits don't lose data."""
        acc = BankAccount(10001, 0)
        threads = []
        
        def worker():
            for _ in range(1000):
                acc.deposit(1)
        
        # Start 10 threads, each depositing 1000 times
        for _ in range(10):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        self.assertEqual(acc.balance, 10000)

if __name__ == '__main__':
    unittest.main()
