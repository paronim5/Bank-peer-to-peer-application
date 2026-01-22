# Step 9: Thread Safety Implementation

## 1. Objective
Ensure the `Bank` class and `BankAccount` operations are thread-safe, as the server will handle multiple clients simultaneously.

## 2. Technical Scope
- **File:** `core/bank.py`
- **Mechanism:** `threading.Lock` / `RLock`

## 3. Implementation Instructions
1.  Import `threading`.
2.  Add `self._lock = threading.RLock()` to `Bank`.
3.  Protect critical sections in `Bank` methods:
    - Account creation (checking for existence then creating).
    - Account removal.
4.  Ensure `BankAccount` methods (`deposit`, `withdraw`) use their own internal locks (already planned in Step 4, but verify here).
5.  Use context managers (`with self._lock:`) for clean code.

## 4. Dependencies
- Step 8 (Bank).

## 5. Validation Criteria
- Run a stress test: Spawn 10 threads trying to create accounts simultaneously. Verify no duplicates and correct count.
- Spawn threads depositing to the same account. Verify final balance is correct.

## 6. Expected Output/Deliverable
- Updated `core/bank.py` with thread safety.
