# Step 25: TCP Server Implementation

## 1. Objective
Implement the main TCP Server that listens for connections and spawns `ClientHandler` threads.

## 2. Technical Scope
- **File:** `network/tcp_server.py`
- **Class:** `TcpServer`

## 3. Implementation Instructions
1.  Create `network/tcp_server.py`.
2.  Constructor: Accepts `host` and `port`.
3.  `start()` method:
    - Create socket (AF_INET, SOCK_STREAM).
    - Bind to host/port.
    - Listen.
    - Loop: `client_sock, addr = server.accept()`.
    - Create `ClientHandler(client_sock, addr)`.
    - Start handler thread.
    - Store handlers in a list (for graceful shutdown).
4.  `stop()` method: Close server socket, stop all handlers.

## 4. Dependencies
- Step 24 (Client Handler).
- Step 2 (Config).

## 5. Validation Criteria
- Start server. Use `telnet` to connect.
- Check if connection is accepted.

## 6. Expected Output/Deliverable
- `network/tcp_server.py`.
