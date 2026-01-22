# Step 15: Command Parser

## 1. Objective
Implement the logic to parse raw incoming strings into a command code and a list of arguments.

## 2. Technical Scope
- **File:** `protocol/command_parser.py`
- **Class:** `CommandParser`

## 3. Implementation Instructions
1.  Create `protocol/command_parser.py`.
2.  Method `parse(raw_data)`:
    - Strip whitespace/newlines.
    - Split by space.
    - First element is Command Code (Validate against Enum).
    - Rest are arguments.
    - Return `(command_code, args_list)`.
3.  Handle empty strings or malformed data gracefully.

## 4. Dependencies
- Step 11 (Enum).

## 5. Validation Criteria
- Test input "AD 10001/10.1.2.3 500".
- Output should be `("AD", ["10001/10.1.2.3", "500"])`.

## 6. Expected Output/Deliverable
- `protocol/command_parser.py`.
