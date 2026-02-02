from typing import List, Tuple
from bank_node.robbery.bank_info import BankInfo
from bank_node.robbery.greedy_strategy import GreedyStrategy
from bank_node.robbery.dp_strategy import DPStrategy

class RobberyPlanner:
    """
    Facade for planning robberies using different strategies.
    """

    def __init__(self, banks: List[BankInfo]):
        self.banks = banks
        self.greedy = GreedyStrategy()
        self.dp = DPStrategy()

    def plan(self, target_amount: int) -> str:
        """
        Plans the robbery to achieve target_amount.
        Selects strategy based on problem size.
        """
        # If number of banks is small enough for DP, use it (Knapsack is pseudo-polynomial)
        # Assuming DP handles the logic. If not, fallback to Greedy.
        
        # For this assignment, let's try Greedy first as it's faster, 
        # or use DP if available. 
        # Let's use DP if < 50 banks, else Greedy.
        
        selected_banks = []
        total_stolen = 0
        total_clients = 0
        
        if len(self.banks) <= 50:
            try:
                selected_banks, total_stolen, total_clients = self.dp.plan(self.banks, target_amount)
            except NotImplementedError:
                selected_banks, total_stolen, total_clients = self.greedy.plan(self.banks, target_amount)
        else:
            selected_banks, total_stolen, total_clients = self.greedy.plan(self.banks, target_amount)
            
        if not selected_banks:
            return f"To achieve {target_amount}, no suitable banks found."

        bank_ips = " and ".join([b.ip for b in selected_banks])
        return f"To achieve {target_amount}, rob banks {bank_ips}, affecting only {total_clients} clients (Total: {total_stolen})."
