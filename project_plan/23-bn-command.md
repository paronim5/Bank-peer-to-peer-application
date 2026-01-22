# Step 23: Implement BN (Bank Number of Clients) Command

## 1. Objective
Implement `BN` command to get the number of clients.

## 2. Technical Scope
- **File:** `protocol/commands/bn_command.py`
- **Class:** `BNCommand`

## 3. Implementation Instructions
1.  Inherit from `BaseCommand`.
2.  `validate_args()`: None.
3.  `execute_logic()`:
    - Call `bank.get_client_count()`.
    - Return the count.
4.  Response format: `BN <number>`.

## 4. Dependencies
- Step 8 (Bank).

## 5. Validation Criteria
- Input `BN` -> Output `BN 5` (if 5 accounts exist).

## 6. Expected Output/Deliverable
- `protocol/commands/bn_command.py`.
