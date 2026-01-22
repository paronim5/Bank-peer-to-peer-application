# Step 12: Validator Component

## 1. Objective
Create a dedicated validator to enforce protocol rules (IP format, account ranges, number types). This keeps the parsing logic clean.

## 2. Technical Scope
- **File:** `protocol/validator.py`
- **Class:** `Validator`

## 3. Implementation Instructions
1.  Create `protocol/validator.py`.
2.  Implement static methods:
    - `validate_ip(ip_str)`: Regex check for IPv4.
    - `validate_account_number(num)`: Check int and range 10000-99999.
    - `validate_amount(amount)`: Check int and >= 0.
    - `validate_port(port)`: Check range 65525-65535.

## 4. Dependencies
- None.

## 5. Validation Criteria
- Unit tests for valid and invalid IPs (e.g., "10.1.2.3" vs "999.999.999.999").
- Unit tests for account boundaries.

## 6. Expected Output/Deliverable
- `protocol/validator.py`.
