# Step 6: JSON Persistence Implementation

## 1. Objective
Implement the `IDataStore` strategy using JSON files. This is the primary persistence mechanism for the Basic/Essentials level.

## 2. Technical Scope
- **File:** `persistence/json_data_store.py`
- **Class:** `JsonDataStore`
- **Implements:** `IDataStore`

## 3. Implementation Instructions
1.  Create `persistence/json_data_store.py`.
2.  Implement `class JsonDataStore(IDataStore)`.
3.  Constructor accepts `file_path`.
4.  Implement `save_data`:
    - Open file in write mode (`w`).
    - Use `json.dump` with indentation.
    - Handle IOErrors.
5.  Implement `load_data`:
    - Check if file exists.
    - If yes, `json.load`.
    - If no, return empty structure.
    - Handle JSON decode errors (corrupt file).

## 4. Dependencies
- Step 5 (Interface).

## 5. Validation Criteria
- Test saving a dictionary `{'test': 123}`.
- Verify file creation on disk.
- Test loading the file back and getting the same dictionary.

## 6. Expected Output/Deliverable
- `persistence/json_data_store.py`.
