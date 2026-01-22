# Step 30: Proxy Client Implementation

## 1. Objective
Create a `ProxyClient` that can open a connection to another bank, send a command, and retrieve the response.

## 2. Technical Scope
- **File:** `network/proxy_client.py`
- **Class:** `ProxyClient`

## 3. Implementation Instructions
1.  Create `network/proxy_client.py`.
2.  Method `send_command(target_ip, port, command_string)`:
    - Create socket.
    - Connect to `(target_ip, port)`.
    - Set timeout (5s).
    - Send `command_string` (encoded).
    - Receive response.
    - Close socket.
    - Return response string.
3.  Handle `socket.timeout` and `ConnectionRefusedError`. Return `ER Timeout` or `ER Connection failed`.

## 4. Dependencies
- Step 29 (IP Helper).

## 5. Validation Criteria
- Start two bank instances on different ports.
- Use `ProxyClient` script to send command from one to the other.

## 6. Expected Output/Deliverable
- `network/proxy_client.py`.
