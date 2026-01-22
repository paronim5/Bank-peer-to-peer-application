# Step 19: Implement AW (Account Withdrawal) Command

## 1. Objective
Implement `AW` command to withdraw money.

## 2. Technical Scope
- **File:** `protocol/commands/aw_command.py`
- **Class:** `AWCommand`

## 3. Implementation Instructions
1.  Inherit from `BaseCommand`.
2.  `validate_args()`: Same as AD.
3.  `execute_logic()`:
    - Call `bank.withdraw(account_num, amount)`.
    - If `False` or raises error (insufficient funds), raise exception with message.
    - Return `None`.
4.  Response format: `AW`.
5.  Error format: `ER Insufficient funds.`

## 4. Dependencies
- Step 8 (Bank).

## 5. Validation Criteria
- Deposit 500 first.
- Input `AW 10000/127.0.0.1 200` -> Output `AW`.
- Input `AW 10000/127.0.0.1 1000` -> Output `ER ...`.

## 6. Expected Output/Deliverable
- `protocol/commands/aw_command.py`.
