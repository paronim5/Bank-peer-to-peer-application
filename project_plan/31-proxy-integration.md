# Step 31: Integrate Proxy Logic into Commands

## 1. Objective
Modify `AD`, `AW`, and `AB` commands to use the Proxy mechanism when the target account IP does not match the local bank.

## 2. Technical Scope
- **Files:** `protocol/commands/ad_command.py`, `aw_command.py`, `ab_command.py`

## 3. Implementation Instructions
1.  In `execute_logic` of these commands:
    - Parse the IP from the account ID.
    - Check `IPHelper.is_local_ip(target_ip)`.
    - **If Local:** Proceed with existing logic.
    - **If Foreign:**
        - Call `ProxyClient.send_command(target_ip, port, original_command_string)`.
        - Return the response received from the foreign bank directly.

## 4. Dependencies
- Step 30 (Proxy Client).

## 5. Validation Criteria
- Run Bank A (10.1.2.3) and Bank B (10.1.2.5).
- Send `AD 10001/10.1.2.5 500` to Bank A.
- Bank A forwards to Bank B.
- Bank B processes and returns `AD`.
- Bank A returns `AD` to client.

## 6. Expected Output/Deliverable
- Updated command classes with routing logic.
