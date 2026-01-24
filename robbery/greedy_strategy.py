from typing import List, Tuple
from robbery.bank_info import BankInfo

class GreedyStrategy:
    """
    Implements a Greedy algorithm to select banks for robbery.
    The goal is to maximize the total amount stolen without exceeding a target amount.
    The heuristic used is the ratio of Total Amount / Number of Clients (High ratio first).
    However, this specific implementation is a variation of the Knapsack problem where
    we want to fit as much 'value' (money) as possible into a 'capacity' (target_amount),
    but here 'value' and 'weight' are the same (money).
    
    The instruction specifies:
    - Sort banks by ratio (descending).
    - Iterate and select banks until target_amount is met or list exhausted.
    - Constraint: Can only take full bank amount.
    - Goal: Maximize money <= target.
    """

    def plan(self, banks: List[BankInfo], target_amount: int) -> Tuple[List[BankInfo], int, int]:
        """
        Selects banks to rob based on the greedy strategy.

        Args:
            banks (List[BankInfo]): List of available banks.
            target_amount (int): The maximum amount to steal (or target capacity).

        Returns:
            Tuple[List[BankInfo], int, int]: 
                - List of selected banks.
                - Total amount stolen.
                - Total number of clients affected.
        """
        # Sort banks by ratio descending
        sorted_banks = sorted(banks, key=lambda b: b.ratio, reverse=True)
        
        selected_banks = []
        total_stolen = 0
        total_clients = 0
        
        for bank in sorted_banks:
            if total_stolen + bank.total_amount <= target_amount:
                selected_banks.append(bank)
                total_stolen += bank.total_amount
                total_clients += bank.num_clients
                
                # If we exactly hit the target, we can stop early (optional optimization)
                if total_stolen == target_amount:
                    break
                    
        return selected_banks, total_stolen, total_clients
