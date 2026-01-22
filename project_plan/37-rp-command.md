# Step 37: Implement RP (Robbery Plan) Command

## 1. Objective
Implement the `RP` command that orchestrates the scanning and planning.

## 2. Technical Scope
- **File:** `protocol/commands/rp_command.py`
- **Class:** `RPCommand`

## 3. Implementation Instructions
1.  Inherit from `BaseCommand`.
2.  `validate_args()`: Expect `target_amount`.
3.  `execute_logic()`:
    - Instantiate `NetworkScanner`.
    - Call `scanner.scan()`.
    - Instantiate Strategy (Greedy or DP - config decided).
    - Call `strategy.plan()`.
    - Format response: "RP To achieve <target>, rob banks A and B, affecting X clients."
4.  Response format: `RP <message>`.

## 4. Dependencies
- Step 34 (Scanner).
- Step 35/36 (Strategies).

## 5. Validation Criteria
- Input `RP 1000000`.
- System scans, plans, and returns readable text.

## 6. Expected Output/Deliverable
- `protocol/commands/rp_command.py`.
