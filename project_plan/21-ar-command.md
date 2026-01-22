# Step 21: Implement AR (Account Remove) Command

## 1. Objective
Implement `AR` command to remove an account.

## 2. Technical Scope
- **File:** `protocol/commands/ar_command.py`
- **Class:** `ARCommand`

## 3. Implementation Instructions
1.  Inherit from `BaseCommand`.
2.  `validate_args()`: Expect `account_id`.
3.  `execute_logic()`:
    - Check balance using `bank.get_balance`.
    - If balance > 0, raise Error ("Cannot delete account with funds").
    - Call `bank.remove_account(account_num)`.
    - Return `None`.
4.  Response format: `AR`.

## 4. Dependencies
- Step 8 (Bank).

## 5. Validation Criteria
- Try to remove account with money -> Error.
- Withdraw all money, then remove -> Success `AR`.

## 6. Expected Output/Deliverable
- `protocol/commands/ar_command.py`.
