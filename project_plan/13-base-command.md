# Step 13: Base Command Structure (Template Method)

## 1. Objective
Implement the Command Pattern base class using the Template Method pattern. This defines the standard lifecycle of every command execution: Validate -> Execute -> Log -> Respond.

## 2. Technical Scope
- **File:** `protocol/commands/base_command.py`
- **Class:** `BaseCommand` (Abstract)

## 3. Implementation Instructions
1.  Create `protocol/commands/base_command.py`.
2.  Define `class BaseCommand(ABC)`.
3.  Constructor: Accepts `bank` instance and raw `args`.
4.  Define abstract methods:
    - `validate_args(self)`: Raises exception if args are invalid.
    - `execute_logic(self)`: Performs the business logic.
5.  Define the Template Method `execute(self)`:
    ```python
    try:
        self.validate_args()
        result = self.execute_logic()
        return self.format_success(result)
    except ValueError as e:
        return self.format_error(str(e))
    except Exception as e:
        return self.format_error("Internal error")
    ```
6.  Helper methods for formatting responses (`CODE data` vs `CODE`).

## 4. Dependencies
- Step 11 (Command Enum).

## 5. Validation Criteria
- Cannot instantiate `BaseCommand`.
- Concrete subclasses must implement abstract methods.

## 6. Expected Output/Deliverable
- `protocol/commands/base_command.py`.
