# Step 16: Implement BC (Bank Code) Command

## 1. Objective
Implement the `BC` command. It returns the bank's IP address.

## 2. Technical Scope
- **File:** `protocol/commands/bc_command.py`
- **Class:** `BCCommand`

## 3. Implementation Instructions
1.  Inherit from `BaseCommand`.
2.  `validate_args()`: Ensure no args are passed (or ignore them).
3.  `execute_logic()`:
    - Get server IP from `ConfigManager` (or `Bank` instance).
    - Return the IP string.
4.  Response format: `BC <ip>`

## 4. Dependencies
- Step 13 (Base Command).
- Step 2 (Config).

## 5. Validation Criteria
- Input `BC` -> Output `BC 127.0.0.1` (or configured IP).

## 6. Expected Output/Deliverable
- `protocol/commands/bc_command.py`.
