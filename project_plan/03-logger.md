# Step 3: Centralized Logger (Singleton)

## 1. Objective
Implement a robust logging system to track application events, errors, and transaction history. This is critical for debugging and meeting the project's logging requirement.

## 2. Technical Scope
- **File:** `utils/logger.py`
- **Class:** `Logger`
- **Pattern:** Singleton
- **Libraries:** Python's built-in `logging` module.

## 3. Implementation Instructions
1.  Create `utils/logger.py`.
2.  Define the `Logger` class (Singleton).
3.  In `__init__`, configure the standard python logger:
    - Set level based on `ConfigManager` (default DEBUG or INFO).
    - Add a `StreamHandler` for Console output.
    - Add a `FileHandler` for File output (e.g., `bank.log`).
    - Define a format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`.
4.  Provide wrapper methods: `info()`, `debug()`, `warning()`, `error()`.

## 4. Dependencies
- Step 2 (ConfigManager) - to get the log level and file path.

## 5. Validation Criteria
- Run a script that logs a message.
- Check console output.
- Check if the log file is created and contains the formatted message.

## 6. Expected Output/Deliverable
- `utils/logger.py` ready for global use.
