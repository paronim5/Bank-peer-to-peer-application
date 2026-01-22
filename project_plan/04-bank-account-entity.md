# Step 4: Bank Account Entity

## 1. Objective
Define the core data model for a bank account. This is the fundamental "Entity" in our business logic layer.

## 2. Technical Scope
- **File:** `core/bank_account.py`
- **Class:** `BankAccount`

## 3. Implementation Instructions
1.  Create `core/bank_account.py`.
2.  Define `class BankAccount`.
3.  Attributes:
    - `number` (int): 10000-99999 (Validated in constructor or factory).
    - `balance` (int): 0 to max 64-bit int (Default 0).
    - `lock` (threading.Lock): For thread-safe updates (internal use).
4.  Methods:
    - `deposit(amount)`: Adds amount (validates > 0).
    - `withdraw(amount)`: Subtracts amount (validates sufficiency). Returns boolean or raises error.
    - `to_dict()`: specific serialization helper.
    - `from_dict(data)`: static method for deserialization.

## 4. Dependencies
- None.

## 5. Validation Criteria
- Unit tests in `tests/test_bank_account.py`.
- Test depositing negative amounts (should fail).
- Test withdrawing more than balance (should fail).
- Test thread safety (optional at this stage, but good to keep in mind).

## 6. Expected Output/Deliverable
- `core/bank_account.py` with fully tested business rules.
