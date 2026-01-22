# Step 22: Implement BA (Bank Total Amount) Command

## 1. Objective
Implement `BA` command to get the total money in the bank.

## 2. Technical Scope
- **File:** `protocol/commands/ba_command.py`
- **Class:** `BACommand`

## 3. Implementation Instructions
1.  Inherit from `BaseCommand`.
2.  `validate_args()`: None.
3.  `execute_logic()`:
    - Call `bank.get_total_capital()`.
    - Return the sum.
4.  Response format: `BA <number>`.

## 4. Dependencies
- Step 8 (Bank).

## 5. Validation Criteria
- Input `BA` -> Output `BA 0` (if empty) or sum of accounts.

## 6. Expected Output/Deliverable
- `protocol/commands/ba_command.py`.
