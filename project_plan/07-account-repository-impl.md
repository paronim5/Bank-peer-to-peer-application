# Step 7: Account Repository

## 1. Objective
Implement the Repository Pattern to abstract the data layer from the business logic. The Bank class will talk to this Repository, not directly to the JSON file.

## 2. Technical Scope
- **File:** `core/account_repository.py`
- **Class:** `AccountRepository`

## 3. Implementation Instructions
1.  Create `core/account_repository.py`.
2.  Constructor takes an `IDataStore` instance.
3.  Internal storage: Maintain an in-memory dictionary of `BankAccount` objects (`self._accounts`).
4.  Methods:
    - `add_account(account)`: Adds to memory.
    - `get_account(number)`: Returns `BankAccount` or `None`.
    - `remove_account(number)`: Removes from memory.
    - `get_all_accounts()`: Returns list of accounts.
    - `load()`: Calls store.load(), converts dicts to `BankAccount` objects, populates memory.
    - `save()`: Converts `BankAccount` objects to dicts, calls store.save().

## 4. Dependencies
- Step 4 (BankAccount).
- Step 5 (IDataStore).

## 5. Validation Criteria
- Unit test: Add account, retrieve it.
- Unit test: Save, clear memory, Load, verify account is back.

## 6. Expected Output/Deliverable
- `core/account_repository.py`.
