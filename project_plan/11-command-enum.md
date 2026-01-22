# Step 11: Command Enum & Protocol Constants

## 1. Objective
Define the protocol constants and available commands to ensure type safety and avoid magic strings throughout the codebase.

## 2. Technical Scope
- **File:** `protocol/command_enum.py`
- **Class:** `CommandType` (Enum)

## 3. Implementation Instructions
1.  Create `protocol/command_enum.py`.
2.  Define `class CommandType(Enum)`.
3.  Add members:
    - `BC = "BC"`
    - `AC = "AC"`
    - `AD = "AD"`
    - `AW = "AW"`
    - `AB = "AB"`
    - `AR = "AR"`
    - `BA = "BA"`
    - `BN = "BN"`
    - `RP = "RP"`
4.  Add a static method to check if a string is a valid command.

## 4. Dependencies
- None.

## 5. Validation Criteria
- Import `CommandType` and verify all protocol commands are present.

## 6. Expected Output/Deliverable
- `protocol/command_enum.py`.
