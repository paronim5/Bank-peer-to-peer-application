import unittest
from bank_node.robbery.bank_info import BankInfo
from bank_node.robbery.dp_strategy import DPStrategy

class TestDpStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = DPStrategy()

    def test_plan_basic_knapsack(self):
        # Classic knapsack
        # Bank A: 2000, 10 clients
        # Bank B: 3000, 20 clients
        # Bank C: 4000, 30 clients
        # Target: 5000
        # Optimal money: A + B = 5000 (30 clients)
        # (C is 4000, less than 5000. A+C=6000 > 5000. B+C=7000 > 5000)
        
        banks = [
            BankInfo("A", 65525, 2000, 10),
            BankInfo("B", 65525, 3000, 20),
            BankInfo("C", 65525, 4000, 30)
        ]
        
        selected, total_stolen, total_clients = self.strategy.plan(banks, 5000)
        
        self.assertEqual(total_stolen, 5000)
        self.assertEqual(total_clients, 30)
        self.assertEqual(len(selected), 2)
        ips = sorted([b.ip for b in selected])
        self.assertEqual(ips, ["A", "B"])

    def test_minimize_clients(self):
        # Two ways to get 1000:
        # 1. Bank A (1000, 100 clients)
        # 2. Bank B (1000, 10 clients)
        # Should pick B.
        
        banks = [
            BankInfo("A", 65525, 1000, 100),
            BankInfo("B", 65525, 1000, 10)
        ]
        
        selected, total_stolen, total_clients = self.strategy.plan(banks, 1000)
        
        self.assertEqual(total_stolen, 1000)
        self.assertEqual(total_clients, 10)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].ip, "B")

    def test_complex_minimization(self):
        # Target 100
        # Option 1: A(50, 1) + B(50, 1) = 100, 2 clients
        # Option 2: C(100, 5) = 100, 5 clients
        # Should pick A and B.
        
        banks = [
            BankInfo("A", 65525, 50, 1),
            BankInfo("B", 65525, 50, 1),
            BankInfo("C", 65525, 100, 5)
        ]
        
        selected, total_stolen, total_clients = self.strategy.plan(banks, 100)
        
        self.assertEqual(total_stolen, 100)
        self.assertEqual(total_clients, 2)
        ips = sorted([b.ip for b in selected])
        self.assertEqual(ips, ["A", "B"])

    def test_greedy_fails_dp_succeeds(self):
        # Greedy by ratio usually fails here:
        # A: 60, 1 client (Ratio 60)
        # B: 100, 10 clients (Ratio 10)
        # C: 120, 30 clients (Ratio 4)
        # Target: 220
        # Greedy picks A (60). Remaining 160. Picks B (100). Total 160. (C doesn't fit).
        # Optimal: B + C = 220.
        
        banks = [
            BankInfo("A", 65525, 60, 1),
            BankInfo("B", 65525, 100, 10),
            BankInfo("C", 65525, 120, 30)
        ]
        
        selected, total_stolen, total_clients = self.strategy.plan(banks, 220)
        
        self.assertEqual(total_stolen, 220)
        ips = sorted([b.ip for b in selected])
        self.assertEqual(ips, ["B", "C"])

    def test_no_solution_fits(self):
        banks = [BankInfo("A", 65525, 1000, 10)]
        selected, total_stolen, total_clients = self.strategy.plan(banks, 500)
        self.assertEqual(total_stolen, 0)
        self.assertEqual(len(selected), 0)

    def test_empty_input(self):
        selected, total_stolen, total_clients = self.strategy.plan([], 1000)
        self.assertEqual(total_stolen, 0)

if __name__ == '__main__':
    unittest.main()
