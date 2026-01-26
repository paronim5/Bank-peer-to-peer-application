# Bank Peer-to-Peer Application - Usage Guide

This guide provides instructions on how to start the Bank Node, connect to it using PuTTY, and interact with the banking protocol.

## 1. Prerequisites

- **Python 3.x** installed.
- **PuTTY** (or any TCP client like Telnet or Netcat) installed.

## 2. Starting the Bank Node

The Bank Node acts as a server that listens for incoming connections.

1.  Open a terminal (PowerShell or Command Prompt).
2.  Navigate to the project root directory.
3.  Run the main application script:

    ```powershell
    # Ensure you are in the project root
    $env:PYTHONPATH = "."
    py bank_node/main.py
    ```

    *Note: If you encounter module errors, ensure `PYTHONPATH` includes the project root or run it exactly as shown above.*

4.  You should see output indicating the server has started:
    ```
    ... - Main - INFO - Starting TCP Server on 127.0.0.1:65525...
    TCP Server listening on 127.0.0.1:65525
    ```

## 3. Connecting with PuTTY

To send commands to your bank, you need to establish a TCP connection.

1.  Open **PuTTY**.
2.  **Host Name (or IP address)**: `127.0.0.1`
3.  **Port**: `65525` (Default, check `bank_node/config.json` if changed).
4.  **Connection type**: Select **Raw** (or **Telnet**).
5.  Click **Open**.

A terminal window will open. You can now type protocol commands.

## 4. Connecting to Other Banks

**Current Status:**
The application is currently operating as a **Standalone Bank Node**. Automatic peer discovery and inter-bank communication (Peer-to-Peer) are planned for future modules (Network Scanner, Proxy Client) and are **not yet automatically enabled**.

**To Simulate Multiple Banks:**
If you want to run multiple banks on the same machine:
1.  Copy the project to a separate folder.
2.  Modify `bank_node/config.json` in the new folder to use a different port (e.g., `65526`).
3.  Run the second instance.
4.  Connect to it using a new PuTTY window on the new port.

## 5. Available Commands

Once connected via PuTTY, you can use the following commands:

| Command | Description | Usage | Example |
| :--- | :--- | :--- | :--- |
| **BC** | **Bank Code**: Returns the Bank's IP address. | `BC` | `BC` -> `BC 127.0.0.1` |
| **AC** | **Account Create**: Creates a new account. | `AC` | `AC` -> `AC 10001/65525` |
| **AD** | **Account Deposit**: Deposits money. | `AD <account_id> <amount>` | `AD 10001/127.0.0.1 500` |
| **AW** | **Account Withdraw**: Withdraws money. | `AW <account_id> <amount>` | `AW 10001/127.0.0.1 200` |
| **AB** | **Account Balance**: Checks account balance. | `AB <account_id>` | `AB 10001/127.0.0.1` |
| **AR** | **Account Remove**: Removes an account (must be empty). | `AR <account_id>` | `AR 10001/127.0.0.1` |
| **BA** | **Bank Amount**: Shows total capital in the bank. | `BA` | `BA` |
| **BN** | **Bank Number**: Shows number of clients. | `BN` | `BN` |

*Note: `<account_id>` format is usually `<account_number>/<ip_address>` (e.g., `10001/127.0.0.1`).*
