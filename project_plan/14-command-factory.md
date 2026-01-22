# Step 14: Command Factory

## 1. Objective
Implement the Factory Pattern to instantiate the correct Command object based on the input string.

## 2. Technical Scope
- **File:** `protocol/command_factory.py`
- **Class:** `CommandFactory`

## 3. Implementation Instructions
1.  Create `protocol/command_factory.py`.
2.  Import all command classes (to be created later, use placeholders for now or implement dynamically).
3.  Method `get_command(command_code, args_list)`:
    - Switch/If-Else on `command_code`.
    - Returns instance of specific command (e.g., `BCCommand(bank, args)`).
    - Returns `None` or raises error if unknown command.

## 4. Dependencies
- Step 13 (Base Command).

## 5. Validation Criteria
- Test with dummy command classes.
- Ensure correct mapping from string "BC" to class `BCCommand`.

## 6. Expected Output/Deliverable
- `protocol/command_factory.py`.
