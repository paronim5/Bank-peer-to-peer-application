from typing import List, Tuple, Optional
from robbery.bank_info import BankInfo

class DpStrategy:
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

        # dp[w] = min_clients to achieve exactly amount w.
        # Initialize with infinity, except dp[0] = 0.
        dp = [float('inf')] * (target_amount + 1)
        dp[0] = 0

        # To reconstruct the solution, we track which bank was added to reach state w.
        # parent[w] = (previous_amount, bank_index_in_original_list)
        parent = [None] * (target_amount + 1)

        # Iterate through each bank (0/1 Knapsack logic)
        for i, bank in enumerate(banks):
            money = bank.total_amount
            clients = bank.num_clients
            
            # We iterate backwards to avoid using the same bank multiple times for the same amount
            for w in range(target_amount, money - 1, -1):
                # If the previous state (w - money) is reachable
                if dp[w - money] != float('inf'):
                    new_clients = dp[w - money] + clients
                    # If we found a way to reach amount w with fewer clients, update it
                    if new_clients < dp[w]:
                        dp[w] = new_clients
                        parent[w] = (w - money, i)

        # Find the best achievable amount <= target_amount
        best_amount = 0
        min_clients_for_best = float('inf')

        # We want the largest amount possible.
        # If there are multiple ways to get the largest amount, dp[best_amount] already stores the min clients.
        for w in range(target_amount, -1, -1):
            if dp[w] != float('inf'):
                best_amount = w
                min_clients_for_best = dp[w]
                break
        
        if best_amount == 0:
            return [], 0, 0

        # Reconstruct the solution
        selected_banks = []
        curr = best_amount
        
        # We need to be careful with reconstruction because 'parent' only stores the LAST update.
        # However, since we process banks in order, and update backwards, simply following parent pointers
        # might get tricky if we overwrote a path. 
        # Actually, standard 1D array DP reconstruction usually requires a 2D table or a slightly different approach 
        # (keeping a list of items for each state, which is memory heavy).
        # OR we can use the standard 2D DP table approach for easier reconstruction.
        # Given the prompt asks for "Standard 0/1 Knapsack DP", 2D is safer for reconstruction.
        # Let's switch to 2D DP logic but optimize space if possible, or just use 2D for clarity/correctness.
        # "dp[i][w]" approach.
        
        # Let's redo with 2D logic to ensure correct reconstruction.
        n = len(banks)
        # dp[i][w] = min_clients using subset of first i banks to get amount w.
        # We can use a dictionary of dictionaries to save space if w is sparse, 
        # but list of lists is standard if target_amount is not too huge. 
        # Assuming target_amount fits in memory.
        
        # Using a 2D table for reconstruction: keep_table[i][w] = boolean (did we include bank i?)
        # And we only need 1D array for the values if we iterate carefully, but 2D is best for reconstruction.
        
        # Optimized approach for Python:
        # dp[w] stores (min_clients, list_of_bank_indices)
        # But list copying is expensive.
        
        # Let's stick to the parent pointer approach but we need to store WHICH iteration (bank index) caused the update?
        # My previous parent[w] stored (w-money, i). This implies that to reach w, we used bank i and came from w-money.
        # BUT, did we reach w-money using bank i? No, because we iterate backwards.
        # However, if we overwrite parent[w] with a later bank, we lose the previous path.
        # Wait, if we use a later bank to reach the SAME w with fewer clients, that's good.
        # But what if we need to backtrack from w-money? parent[w-money] might have been overwritten by a later bank too?
        # Yes, 1D array reconstruction is lossy if not careful.
        
        # Correct 2D approach:
        # table[w] = min_clients.
        # keep[i][w] = boolean (True if bank i is included in the optimal set for capacity w)
        
        # Let's use the `keep` table approach.
        dp = [float('inf')] * (target_amount + 1)
        dp[0] = 0
        keep = [[False] * (target_amount + 1) for _ in range(n)]
        
        for i, bank in enumerate(banks):
            money = bank.total_amount
            clients = bank.num_clients
            for w in range(target_amount, money - 1, -1):
                if dp[w - money] != float('inf'):
                    if dp[w - money] + clients < dp[w]:
                        dp[w] = dp[w - money] + clients
                        keep[i][w] = True
                    # Else: keep[i][w] remains False (we don't include bank i for amount w, or previous combo was better)

        # Find best amount again
        best_amount = 0
        for w in range(target_amount, -1, -1):
            if dp[w] != float('inf'):
                best_amount = w
                break
        
        if best_amount == 0:
            return [], 0, 0
            
        # Reconstruct
        selected_banks_indices = []
        curr_w = best_amount
        for i in range(n - 1, -1, -1):
            if keep[i][curr_w]:
                selected_banks_indices.append(i)
                curr_w -= banks[i].total_amount
        
        # Map indices back to bank objects
        # Indices are added in reverse order of iteration, so reverse to match roughly
        selected_banks_indices.reverse()
        selected_banks = [banks[i] for i in selected_banks_indices]
        
        return selected_banks, best_amount, dp[best_amount]
