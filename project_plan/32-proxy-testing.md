# Step 32: Testing Essentials (Proxy)

## 1. Objective
Verify the Proxy Forwarding functionality comprehensively.

## 2. Technical Scope
- **Test:** Integration Test with 2 nodes.

## 3. Implementation Instructions
1.  Create a test script `tests/test_proxy.py`.
2.  Start two servers on different ports (e.g., 65525, 65526) in separate threads/processes.
3.  Connect to Server 1.
4.  Create account on Server 2 (requires sending `AC` to Server 2 directly first, as `AC` is not proxied).
5.  Send `AB <server2_acc>/<server2_ip>` to Server 1.
6.  Verify correct balance is returned.

## 4. Dependencies
- Step 31 (Proxy Integration).

## 5. Validation Criteria
- Successful cross-node communication.

## 6. Expected Output/Deliverable
- Verified Essentials Level Bank Node.
