# Step 5: Persistence Interface (Strategy Pattern)

## 1. Objective
Define the interface for data storage. This implements the Strategy Pattern, allowing us to swap between JSON, SQLite, or CSV storage without changing the business logic.

## 2. Technical Scope
- **File:** `persistence/i_data_store.py`
- **Class:** `IDataStore` (Abstract Base Class)

## 3. Implementation Instructions
1.  Create `persistence/i_data_store.py`.
2.  Import `ABC` and `abstractmethod` from `abc`.
3.  Define `class IDataStore(ABC)`.
4.  Define abstract methods:
    - `save_data(self, data: dict)`: Saves the entire bank state.
    - `load_data(self) -> dict`: Loads the bank state.
5.  Define the expected data structure for `dict` (e.g., `{'accounts': {...}}`).

## 4. Dependencies
- None.

## 5. Validation Criteria
- This is an interface; it cannot be instantiated.
- Validation involves creating a dummy concrete class in a test to ensure it enforces method implementation.

## 6. Expected Output/Deliverable
- `persistence/i_data_store.py`.
