# Step 29: IP Helper & Detection Logic

## 1. Objective
Implement utilities to detect if a target IP is "local" (this bank) or "foreign" (another bank). This is the foundation for the Proxy (Essentials) level.

## 2. Technical Scope
- **File:** `utils/ip_helper.py`

## 3. Implementation Instructions
1.  Create `utils/ip_helper.py`.
2.  Function `is_local_ip(ip_address)`:
    - Compare `ip_address` with the server's configured IP.
    - Handle `127.0.0.1` vs `localhost` vs actual LAN IP.
    - Ideally, checking against the configured `server.ip` from ConfigManager is sufficient.

## 4. Dependencies
- Step 2 (Config).

## 5. Validation Criteria
- Test `is_local_ip` with matching and non-matching IPs.

## 6. Expected Output/Deliverable
- `utils/ip_helper.py`.
