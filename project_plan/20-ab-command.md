# Step 20: Implement AB (Account Balance) Command

## 1. Objective
Implement `AB` command to check balance.

## 2. Technical Scope
- **File:** `protocol/commands/ab_command.py`
- **Class:** `ABCommand`

## 3. Implementation Instructions
1.  Inherit from `BaseCommand`.
2.  `validate_args()`: Expect `account_id`.
3.  `execute_logic()`:
    - Call `bank.get_balance(account_num)`.
    - Return balance amount.
4.  Response format: `AB <number>`.

## 4. Dependencies
- Step 8 (Bank).

## 5. Validation Criteria
- Input `AB 10000/127.0.0.1` -> Output `AB 300` (assuming previous steps).

## 6. Expected Output/Deliverable
- `protocol/commands/ab_command.py`.
