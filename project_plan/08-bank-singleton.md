# Step 8: Bank Manager (Singleton)

## 1. Objective
Implement the central `Bank` class using the Singleton pattern. This class acts as the Facade for all banking operations.

## 2. Technical Scope
- **File:** `core/bank.py`
- **Class:** `Bank`
- **Pattern:** Singleton

## 3. Implementation Instructions
1.  Create `core/bank.py`.
2.  Implement Singleton pattern.
3.  Initialize with `AccountRepository` and `ConfigManager`.
4.  Core Methods:
    - `create_account()`: Generates unique ID (10000-99999), creates `BankAccount`, adds to repo.
    - `get_balance(account_number)`: Returns balance.
    - `deposit(account_number, amount)`: Delegated to account.
    - `withdraw(account_number, amount)`: Delegated to account.
    - `transfer(...)`: (Not strictly required by protocol but good for internal logic if needed).
    - `get_total_capital()`: Sums all account balances (for BA command).
    - `get_client_count()`: Returns count (for BN command).

## 4. Dependencies
- Step 7 (Repository).
- Step 2 (Config).

## 5. Validation Criteria
- Test creating unique accounts.
- Test `get_total_capital` sums correctly.

## 6. Expected Output/Deliverable
- `core/bank.py`.
