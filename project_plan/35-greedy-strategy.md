# Step 35: Greedy Robbery Strategy

## 1. Objective
Implement the Greedy algorithm to solve the Knapsack problem for the Robbery Plan.

## 2. Technical Scope
- **File:** `robbery/greedy_strategy.py`
- **Class:** `GreedyStrategy`

## 3. Implementation Instructions
1.  Create `robbery/greedy_strategy.py`.
2.  Method `plan(banks: List[BankInfo], target_amount: int)`:
    - Sort banks by `ratio` (descending).
    - Iterate and select banks until `target_amount` is met or list exhausted.
    - **Constraint:** Can only take *full* bank amount.
    - Goal: Maximize money <= target. (Wait, standard Knapsack is Max Value within Weight capacity. Here, value=money, weight=money. So we want Max Money <= Target).
    - Actually, the Greedy approach for 0/1 Knapsack is not always optimal, but it's a required heuristic.
    - Return `(list_of_banks_to_rob, total_stolen, total_clients)`.

## 4. Dependencies
- Step 33 (BankInfo).

## 5. Validation Criteria
- Test with known dataset. Verify it picks high-ratio banks first.

## 6. Expected Output/Deliverable
- `robbery/greedy_strategy.py`.
