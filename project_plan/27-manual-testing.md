# Step 27: Manual System Testing

## 1. Objective
Verify the Basic Bank Node functionality using manual tools like PuTTY or Telnet.

## 2. Technical Scope
- **Tools:** PuTTY, Telnet, or Netcat.
- **Process:** Manual verification.

## 3. Implementation Instructions
1.  Start the server.
2.  Connect via Telnet: `telnet localhost 65525`.
3.  Type `BC` -> Expect `BC 127.0.0.1`.
4.  Type `AC` -> Expect `AC 10000/127.0.0.1`.
5.  Type `AD 10000/127.0.0.1 1000` -> Expect `AD`.
6.  Type `AB 10000/127.0.0.1` -> Expect `AB 1000`.
7.  Restart Server.
8.  Check `AB` again -> Balance should persist.

## 4. Dependencies
- Step 26 (Running App).

## 5. Validation Criteria
- All commands work as expected in a real terminal session.

## 6. Expected Output/Deliverable
- A verified, working Basic Bank Node.
