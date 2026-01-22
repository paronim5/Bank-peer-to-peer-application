# Step 26: Application Entry Point (Main)

## 1. Objective
Wire everything together in `main.py`. Initialize config, logger, bank, and server.

## 2. Technical Scope
- **File:** `main.py`

## 3. Implementation Instructions
1.  Load `ConfigManager`.
2.  Initialize `Logger`.
3.  Initialize `Bank` (which loads data).
4.  Initialize `TcpServer` with config values.
5.  Start Server in a `try/except KeyboardInterrupt` block.
6.  Ensure graceful shutdown on Ctrl+C.

## 4. Dependencies
- All previous steps.

## 5. Validation Criteria
- Run `python main.py`.
- Server starts and prints "Listening on ...".

## 6. Expected Output/Deliverable
- `main.py`.
