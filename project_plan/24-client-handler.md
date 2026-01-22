# Step 24: Client Handler (Thread)

## 1. Objective
Create the `ClientHandler` class to manage individual client connections. This runs in a separate thread for each client.

## 2. Technical Scope
- **File:** `network/client_handler.py`
- **Class:** `ClientHandler`
- **Inherits:** `threading.Thread`

## 3. Implementation Instructions
1.  Create `network/client_handler.py`.
2.  Constructor: Accepts `socket` and `address`.
3.  `run()` method:
    - Loop to receive data (`socket.recv`).
    - Decode UTF-8.
    - Check for newline `\n` to identify message boundaries (buffer handling).
    - Pass raw string to `CommandParser`.
    - Use `CommandFactory` to get command.
    - Execute command.
    - Send response back (encode UTF-8).
    - Handle `ConnectionResetError` or empty bytes (client disconnect).
4.  Implement timeout logic (socket timeout).

## 4. Dependencies
- Step 14 (Factory).
- Step 15 (Parser).

## 5. Validation Criteria
- Mock a socket. Send "BC\n". Verify `run` loop processes it and sends back "BC ...\n".

## 6. Expected Output/Deliverable
- `network/client_handler.py`.
