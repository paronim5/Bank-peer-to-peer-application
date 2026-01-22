# Step 17: Implement AC (Account Create) Command

## 1. Objective
Implement `AC` command to create new accounts.

## 2. Technical Scope
- **File:** `protocol/commands/ac_command.py`
- **Class:** `ACCommand`

## 3. Implementation Instructions
1.  Inherit from `BaseCommand`.
2.  `validate_args()`: None required.
3.  `execute_logic()`:
    - Call `bank.create_account()`.
    - Get the new account number.
    - Get server IP.
    - Return formatted string `number/ip`.
4.  Response format: `AC <number>/<ip>`

## 4. Dependencies
- Step 8 (Bank).

## 5. Validation Criteria
- Input `AC` -> Output `AC 10000/127.0.0.1`.

## 6. Expected Output/Deliverable
- `protocol/commands/ac_command.py`.
