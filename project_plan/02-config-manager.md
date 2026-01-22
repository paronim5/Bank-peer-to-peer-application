# Step 2: Configuration Manager (Singleton)

## 1. Objective
Implement a centralized `ConfigManager` using the Singleton pattern to manage application settings. This ensures all components access the same configuration and allows for hot-reloading if needed (bonus).

## 2. Technical Scope
- **File:** `core/config_manager.py`
- **Class:** `ConfigManager`
- **Pattern:** Singleton

## 3. Implementation Instructions
1.  Create `core/config_manager.py`.
2.  Define the `ConfigManager` class.
3.  Implement the Singleton pattern (ensure `__new__` or a class method returns the same instance).
4.  Implement a `load_config(self, path='config.json')` method to read the JSON file.
5.  Store configuration in a dictionary attribute (e.g., `self.config`).
6.  Add getter methods (e.g., `get(self, key, default=None)`).
7.  Ensure it handles `FileNotFoundError` by falling back to hardcoded defaults or raising a critical error.

## 4. Dependencies
- Step 1 (Project Structure).

## 5. Validation Criteria
- Create a test script `tests/test_config.py`.
- Verify that `ConfigManager()` returns the same instance twice (`a is b`).
- Verify that values from `config.json` are correctly loaded.

## 6. Expected Output/Deliverable
- `core/config_manager.py` with a functional Singleton class.
