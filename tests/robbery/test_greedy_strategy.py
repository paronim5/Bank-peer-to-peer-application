import unittest
from robbery.bank_info import BankInfo
from robbery.greedy_strategy import GreedyStrategy

class TestGreedyStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = GreedyStrategy()

    def test_plan_basic(self):
        # Bank A: 1000 / 10 = 100
        # Bank B: 500 / 2 = 250 (Highest Ratio)
        # Bank C: 2000 / 50 = 40
        banks = [
            BankInfo("1.1.1.1", 1000, 10),
            BankInfo("1.1.1.2", 500, 2),
            BankInfo("1.1.1.3", 2000, 50)
        ]
        
        # Target 1600
        # Should pick B (500) first. Remaining: 1100.
        # Next highest is A (1000). Remaining: 100.
        # Next is C (2000). Too big. Skip.
        # Total: 1500.
        
        selected, total_stolen, total_clients = self.strategy.plan(banks, 1600)
        
        self.assertEqual(len(selected), 2)
        self.assertEqual(total_stolen, 1500)
        self.assertEqual(total_clients, 12) # 2 + 10
        
        # Verify order: B then A
        self.assertEqual(selected[0].ip, "1.1.1.2")
        self.assertEqual(selected[1].ip, "1.1.1.1")

    def test_plan_exact_match(self):
        banks = [BankInfo("1.1.1.1", 1000, 10)]
        selected, total_stolen, total_clients = self.strategy.plan(banks, 1000)
        self.assertEqual(len(selected), 1)
        self.assertEqual(total_stolen, 1000)

    def test_plan_none_fit(self):
        banks = [BankInfo("1.1.1.1", 1000, 10)]
        selected, total_stolen, total_clients = self.strategy.plan(banks, 500)
        self.assertEqual(len(selected), 0)
        self.assertEqual(total_stolen, 0)

    def test_plan_empty_list(self):
        selected, total_stolen, total_clients = self.strategy.plan([], 1000)
        self.assertEqual(len(selected), 0)
        self.assertEqual(total_stolen, 0)

    def test_plan_zero_clients_ratio(self):
        # Handle division by zero case in BankInfo (ratio 0.0)
        banks = [
            BankInfo("1.1.1.1", 1000, 0), # Ratio 0
            BankInfo("1.1.1.2", 100, 1)   # Ratio 100
        ]
        # Should pick B first
        selected, total_stolen, total_clients = self.strategy.plan(banks, 2000)
        self.assertEqual(selected[0].ip, "1.1.1.2")
        self.assertEqual(selected[1].ip, "1.1.1.1")

if __name__ == '__main__':
    unittest.main()
