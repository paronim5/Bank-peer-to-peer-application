# Step 33: Bank Info & Robbery Models

## 1. Objective
Prepare the data structures for the "Hacker" level Robbery Plan. We need a way to store discovered bank information (IP, Total Amount, Client Count).

## 2. Technical Scope
- **File:** `robbery/bank_info.py`
- **Class:** `BankInfo` (DTO)

## 3. Implementation Instructions
1.  Create `robbery/bank_info.py`.
2.  Define `class BankInfo`:
    - Attributes: `ip`, `total_amount` (int), `num_clients` (int).
    - Property `ratio`: `total_amount / num_clients` (handle div by zero).
    - Method `__repr__`: specific string representation.

## 4. Dependencies
- None.

## 5. Validation Criteria
- Create instances and check ratio calculation.

## 6. Expected Output/Deliverable
- `robbery/bank_info.py`.
