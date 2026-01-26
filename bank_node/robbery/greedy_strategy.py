from typing import List, Tuple
from bank_node.robbery.bank_info import BankInfo

class GreedyStrategy:
    """
    Implements the Greedy algorithm for the Robbery Plan.
    Prioritizes banks with higher money-to-client ratio.
    """

    def plan(self, banks: List[BankInfo], target_amount: int) -> Tuple[List[BankInfo], int, int]:
        """
        Selects banks to rob to reach the target amount using a greedy approach.
        
        Args:
            banks: List of discovered banks.
            target_amount: The target amount of money to steal.
            
        Returns:
            Tuple containing:
            - List of banks to rob.
            - Total amount stolen.
            - Total clients affected.
        """
        # Sort banks by ratio (descending)
        # Ratio = total_amount / num_clients (maximize money per client)
        sorted_banks = sorted(banks, key=lambda b: b.ratio, reverse=True)
        
        selected_banks = []
        current_amount = 0
        current_clients = 0
        
        for bank in sorted_banks:
            # Check if adding this bank exceeds target?
            # The prompt says: "Maximize robbed money (<= target amount)"
            # So we stop if adding the next bank would exceed the target.
            
            if current_amount + bank.total_amount <= target_amount:
                selected_banks.append(bank)
                current_amount += bank.total_amount
                current_clients += bank.num_clients
            
            # If we exactly met the target, we can stop early
            if current_amount == target_amount:
                break
                
        return selected_banks, current_amount, current_clients
