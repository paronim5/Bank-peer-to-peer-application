# Step 10: Observer Pattern & Auto-Saver

## 1. Objective
Implement the Observer pattern to notify components of bank events. Specifically, create an `AutoSaver` that saves data whenever a transaction occurs (or periodically).

## 2. Technical Scope
- **File:** `core/bank.py` (Subject), `persistence/auto_saver.py` (Observer)
- **Pattern:** Observer

## 3. Implementation Instructions
1.  **Modify Bank:**
    - Add `subscribe(observer)` and `unsubscribe(observer)`.
    - Add `notify(event_type, data)`.
    - Call `notify` after `create_account`, `deposit`, `withdraw`.
2.  **Create AutoSaver:**
    - Create `persistence/auto_saver.py`.
    - `class AutoSaver`: Implements an `update` method.
    - In `update`, call `account_repository.save()`.
    - Ideally, run the save in a separate thread or debounced to avoid disk I/O blocking the main thread on every transaction (optional optimization).

## 4. Dependencies
- Step 8 (Bank).
- Step 7 (Repository).

## 5. Validation Criteria
- Perform a deposit.
- Check if `bank_data.json` is updated automatically without manual save calls.

## 6. Expected Output/Deliverable
- `persistence/auto_saver.py`.
- Updated `core/bank.py`.
