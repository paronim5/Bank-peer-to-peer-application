# Step 34: Network Scanner Implementation

## 1. Objective
Implement the scanning logic to discover other banks in the network. This involves probing a range of IPs with `BC`, then `BA`, then `BN`.

## 2. Technical Scope
- **File:** `network/network_scanner.py`
- **Class:** `NetworkScanner`

## 3. Implementation Instructions
1.  Create `network/network_scanner.py`.
2.  Method `scan(ip_range_start, ip_range_end)`:
    - Loop through IPs.
    - For each IP, use `ProxyClient` (or similar simple socket) to send `BC`.
    - If response is `BC ...`:
        - Send `BA`. Parse result.
        - Send `BN`. Parse result.
        - Create `BankInfo` object.
        - Add to list.
    - Use threading (ThreadPoolExecutor) to scan fast! Scanning 255 IPs sequentially is too slow.

## 4. Dependencies
- Step 30 (Proxy Client/Socket logic).
- Step 33 (BankInfo).

## 5. Validation Criteria
- Mock the network (or run local nodes).
- Scanner returns list of `BankInfo` objects for active nodes.

## 6. Expected Output/Deliverable
- `network/network_scanner.py`.
