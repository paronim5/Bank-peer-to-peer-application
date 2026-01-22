# Step 18: Implement AD (Account Deposit) Command

## 1. Objective
Implement `AD` command to deposit money.

## 2. Technical Scope
- **File:** `protocol/commands/ad_command.py`
- **Class:** `ADCommand`

## 3. Implementation Instructions
1.  Inherit from `BaseCommand`.
2.  `validate_args()`:
    - Expect 2 args: `account_id` (format `num/ip`) and `amount`.
    - Parse `account_id` to split number and IP.
    - Check if IP matches local IP (for now, assume local only).
    - Validate `amount` is positive integer.
3.  `execute_logic()`:
    - Call `bank.deposit(account_num, amount)`.
    - Return `None` (success implies empty data for this command).
4.  Response format: `AD` (no data).

## 4. Dependencies
- Step 12 (Validator).

## 5. Validation Criteria
- Input `AD 10000/127.0.0.1 500`.
- Output `AD`.
- Check bank balance updated.

## 6. Expected Output/Deliverable
- `protocol/commands/ad_command.py`.
