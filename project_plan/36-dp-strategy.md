# Step 36: Dynamic Programming Strategy

## 1. Objective
Implement the Dynamic Programming algorithm for the optimal solution to the Robbery Plan (0/1 Knapsack).

## 2. Technical Scope
- **File:** `robbery/dp_strategy.py`
- **Class:** `DpStrategy`

## 3. Implementation Instructions
1.  Create `robbery/dp_strategy.py`.
2.  Method `plan(banks, target_amount)`:
    - Implement Standard 0/1 Knapsack DP.
    - `dp[w]` = max value (money) with capacity `w`.
    - Since value = weight (money = money), we want to find if we can achieve exactly `target_amount` or closest to it.
    - Secondary optimization: Minimize clients.
    - This might need a 2D DP or tracking `(money, clients)` tuples.
    - Logic: `dp[w] = min_clients` to achieve money `w`. Initialize with infinity. `dp[0] = 0`.
    - Find largest `w <= target_amount` where `dp[w]` is not infinity.
    - Reconstruct solution to find which banks.

## 4. Dependencies
- Step 33 (BankInfo).

## 5. Validation Criteria
- Compare results with Greedy on a tricky dataset. DP should always be equal or better (closer to target with fewer clients).

## 6. Expected Output/Deliverable
- `robbery/dp_strategy.py`.
