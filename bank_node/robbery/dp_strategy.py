from typing import List, Tuple
from bank_node.robbery.bank_info import BankInfo

class DPStrategy:
    """
    Implements a Dynamic Programming algorithm (0/1 Knapsack) to select banks for robbery.
    Goal:
    1. Maximize total amount stolen <= target_amount.
    2. If multiple combinations yield the same amount, minimize the total number of clients.
    """

    def plan(self, banks: List[BankInfo], target_amount: int) -> Tuple[List[BankInfo], int, int]:
        """
        Selects banks to rob using DP.

        Args:
            banks (List[BankInfo]): List of available banks.
            target_amount (int): The maximum amount to steal.

        Returns:
            Tuple[List[BankInfo], int, int]: 
                - List of selected banks.
                - Total amount stolen.
                - Total number of clients affected.
        """
        if not banks or target_amount <= 0:
            return [], 0, 0

        n = len(banks)
        # dp[w] = min_clients using subset of banks to get amount w.
        # Initialize with infinity, except dp[0] = 0.
        dp = [float('inf')] * (target_amount + 1)
        dp[0] = 0
        
        # keep[i][w] = boolean (True if bank i is included in the optimal set for capacity w)
        # We need this to reconstruct the solution.
        keep = [[False] * (target_amount + 1) for _ in range(n)]
        
        for i, bank in enumerate(banks):
            money = bank.total_amount
            clients = bank.num_clients
            
            # Skip banks with 0 money or if they exceed target alone (and we loop downwards anyway)
            if money <= 0:
                continue
                
            # Iterate backwards to avoid using the same bank multiple times for the same amount
            for w in range(target_amount, money - 1, -1):
                # If the previous state (w - money) is reachable
                if dp[w - money] != float('inf'):
                    new_clients = dp[w - money] + clients
                    # If we found a way to reach amount w with fewer clients (or first time reaching it), update it
                    # Note: This logic prioritizes MIN clients for the SAME amount.
                    # It does not strictly prioritize MAX amount first. 
                    # But since we scan for BEST amount at the end, it works out.
                    if new_clients < dp[w]:
                        dp[w] = new_clients
                        keep[i][w] = True
                    # Else: keep[i][w] remains False

        # Find best achievable amount <= target_amount
        # We prioritize highest amount first.
        best_amount = 0
        min_clients_for_best = float('inf')

        for w in range(target_amount, -1, -1):
            if dp[w] != float('inf'):
                best_amount = w
                min_clients_for_best = dp[w]
                break
        
        if best_amount == 0:
            return [], 0, 0

        # Reconstruct the solution
        selected_banks_indices = []
        curr_w = best_amount
        for i in range(n - 1, -1, -1):
            if keep[i][curr_w]:
                selected_banks_indices.append(i)
                curr_w -= banks[i].total_amount
        
        selected_banks_indices.reverse()
        selected_banks = [banks[i] for i in selected_banks_indices]
        
        return selected_banks, best_amount, min_clients_for_best
