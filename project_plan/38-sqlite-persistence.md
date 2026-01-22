# Step 38: SQLite Persistence (Bonus)

## 1. Objective
Implement `SqliteDataStore` as an alternative to JSON. This demonstrates the power of the Strategy Pattern.

## 2. Technical Scope
- **File:** `persistence/sqlite_data_store.py`
- **Class:** `SqliteDataStore`
- **Library:** `sqlite3`

## 3. Implementation Instructions
1.  Create `persistence/sqlite_data_store.py`.
2.  Implement `IDataStore`.
3.  `save_data`:
    - Connect to DB.
    - Create tables if not exist.
    - INSERT/UPDATE accounts.
4.  `load_data`:
    - SELECT * FROM accounts.
    - Reconstruct dict structure.

## 4. Dependencies
- Step 5 (Interface).

## 5. Validation Criteria
- Change config to use "sqlite".
- Restart server.
- Data should persist in `.db` file.

## 6. Expected Output/Deliverable
- `persistence/sqlite_data_store.py`.
