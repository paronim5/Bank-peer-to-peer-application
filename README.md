# P2P Bank Node - Complete Requirements for Maximum Points

To achieve the best grade, you must complete **HACKER BANK NODE** + demonstrate excellent architecture, code reuse, and custom extensions.

---

## 1. BASIC TECHNICAL PARAMETERS

### Network Communication
- **Protocol:** TCP/IP
-  **Port:** Any in range **65525-65535** (configurable)
-  **Encoding:** UTF-8 (plain text)
-  **Connection:** Must work via PuTTY/telnet for manual testing
-  **Parallelization:** True physical parallelization (multi-threading), not just concurrency
-  **Multiple clients:** Server must handle multiple connections simultaneously

### Execution
- Must run on school PC **without IDE**
- Functional in school network
- Simple startup method (documented)

---

## 2. COMMUNICATION PROTOCOL (CRITICAL!)

### Protocol Rules
- **Each message is single-line** (ends with `\n`)
- Each command starts with **two-letter code**
- Response starts with **same code** or `ER`
- **Case-sensitive:** MUST work with uppercase, lowercase is bonus

### CRITICAL RULE FOR RESPONSES:

**Commands WITH DATA in response:**
```
Format: CODE<space><data>
Applies to: BC, AC, AB, BA, BN
```

**Commands WITHOUT DATA in response:**
```
Format: CODE (no space, nothing else!)
Applies to: AD, AW, AR
```

### Complete Command Table

| Code | Name | Call | Success Response | Error Response |
|------|------|------|------------------|----------------|
| **BC** | Bank Code | `BC` | `BC <ip>` | `ER <message>` |
| **AC** | Account Create | `AC` | `AC <account>/<ip>` | `ER <message>` |
| **AD** | Account Deposit | `AD <account>/<ip> <number>` | `AD` | `ER <message>` |
| **AW** | Account Withdrawal | `AW <account>/<ip> <number>` | `AW` | `ER <message>` |
| **AB** | Account Balance | `AB <account>/<ip>` | `AB <number>` | `ER <message>` |
| **AR** | Account Remove | `AR <account>/<ip>` | `AR` | `ER <message>` |
| **BA** | Bank Total Amount | `BA` | `BA <number>` | `ER <message>` |
| **BN** | Bank Number of Clients | `BN` | `BN <number>` | `ER <message>` |
| **RP** | Robbery Plan | `RP <number>` | `RP <message>` | `ER <message>` |

### Data Types in Protocol

**`<ip>`**
- Format: `0.0.0.0` to `255.255.255.255`
- Used as **bank code** (unique identifier)

**`<account>`**
- Positive integer: **10000 to 99999**
- Unique within one bank
- Choose as you like (sequential, random, etc.)

**`<number>`**
- Non-negative integer: **0 to 9223372036854775807**
- 64-bit long (signed)
- Currency: **US dollars** (USD)

**`<message>`**
- Any text in Czech or English
- Recommended length: one sentence
- For multiple problems use compound sentence

---

## 3. FUNCTIONAL REQUIREMENTS

### BC - Bank Code
```
Input:  BC
Output: BC 10.1.2.3
```
- Returns server's IP address as bank code
- IP can be detected dynamically OR set in config
- Serves as "ping" - test that banking app is running on PC

### AC - Account Create
```
Input:  AC
Output: AC 10001/10.1.2.3
```
- Creates new account with unique number
- Account number: 10000-99999
- Initial balance: **0**
- Must not repeat within bank

### AD - Account Deposit
```
Input:  AD 10001/10.1.2.3 3000
Output: AD
```
- Deposits money to account
- Amount must be **positive number**
- Response is **just `AD`** (no space!)

### AW - Account Withdrawal
```
Input:  AW 10001/10.1.2.3 2000
Output: AW
```
- Withdraws money from account
- Must check if **sufficient funds** exist
- Response is **just `AW`** (no space!)
- If insufficient funds: `ER Insufficient funds.`

### AB - Account Balance
```
Input:  AB 10001/10.1.2.3
Output: AB 2000
```
- Returns current account balance

### AR - Account Remove
```
Input:  AR 10001/10.1.2.3
Output: AR
```
- Deletes account **ONLY if balance = 0**
- Response is **just `AR`** (no space!)
- If balance > 0: `ER Cannot delete account with funds.`

### BA - Bank Total Amount
```
Input:  BA
Output: BA 7001211
```
- Returns **total sum** of all money on all accounts

### BN - Bank Number of Clients
```
Input:  BN
Output: BN 5
```
- Returns **number of accounts** (clients) in bank

### RP - Robbery Plan (HACKER level)
```
Input:  RP 1000000
Output: RP To achieve 1000000, rob banks 10.1.2.3 and 10.1.2.85, affecting only 21 clients.
```

**Algorithm:**
1. **Discover network state:**
   - Scan network (IP address range)
   - For each bank get: total sum (BA) and number of clients (BN)
   
2. **Key constraint:**
   - **You can rob ALWAYS AND ONLY entire bank or nothing!**
   - Cannot take just part of money from a bank
   
3. **Optimization goals (in this order):**
   - Primary: **Maximize robbed money** (≤ target amount)
   - Secondary: **Minimize number of affected clients**
   - Tertiary: **Minimize number of robbed banks**

4. **Problem type:**
   - **0/1 Knapsack Problem**
   - Knapsack capacity = target amount
   - Each bank = item (value = sum, weight = sum)
   - Goal: max value with min items/clients

5. **Solution:**
   - **Greedy approach:** Sort banks by ratio (sum/clients), take largest
   - **Dynamic Programming:** For optimal solution (more complex, but better)

---

## 4. DIFFICULTY LEVELS

### BASIC BANK NODE (max grade 3-4)
**What must work:**
- All commands: BC, AC, AD, AW, AB, AR, BA, BN
- Correct protocol (response format!)
- Data persistence (survives restart)
- Multi-threading (parallel client handling)
- Timeouts
- Logging
- Configuration (port, IP)

**Persistence:**
- Accounts and balances **must not be lost** on restart
- Technology choice is yours: JSON, XML, SQLite, CSV...
- **Important:** Suitable architecture for chosen storage!

---

### ESSENTIALS BANK NODE (max grade 2-3)
**BASIC +:**

**Proxy forwarding for AD, AW, AB:**
```
Scenario:
1. Your bank has IP 10.1.2.3
2. Command arrives: AD 10001/10.1.2.5 1000
3. IP 10.1.2.5 ≠ your IP
4. Your server:
   - Connects to 10.1.2.5
   - Sends: AD 10001/10.1.2.5 1000
   - Receives response
   - Returns response to original client
```

**Implementation:**
- Automatic detection if IP = local or foreign
- Create **outgoing** TCP connection to foreign bank
- Timeout on proxy requests (5s default)
- Proper error propagation

---

### HACKER BANK NODE 
**ESSENTIALS +:**

**RP - Robbery Plan:**
- Implementation of `RP <number>` command
- **Network scanning:**
  - Automatic bank detection in network
  - IP address range (configurable, e.g., 10.1.2.1-254)
  - For each IP: try BC, if works → get BA and BN
  - Timeout on each IP (fast scanning!)
  
- **Optimization algorithm:**
  - Input: list of banks with sums and client counts
  - Output: optimal combination of banks to rob
  - **Recommendation:** Start with greedy, then possibly DP
  
- **Response format:**
  - Readable text with details
  - Example: `RP To achieve 1000000, rob banks 10.1.2.3 and 10.1.2.85, affecting only 21 clients.`

---

## 5. RECOMMENDED ARCHITECTURE: LAYERED ARCHITECTURE + REPOSITORY PATTERN

**Layered Architecture** (3-Layer):
- ✅ **Separation of concerns** - each layer has specific responsibility
- ✅ **Easy to test** - can test each layer independently
- ✅ **Easy to maintain** - changes in one layer don't affect others
- ✅ **Easy to understand** - clear structure

**Layers:**
1. **Presentation Layer** (Network/Protocol) - handles TCP communication
2. **Business Logic Layer** (Core) - handles bank operations
3. **Data Access Layer** (Persistence) - handles data storage


---

## 6. DESIGN PATTERNS TO USE

### Essential Patterns (Must Use):

**1. Singleton Pattern**
- **Where:** Bank, Logger, ConfigManager
- **Why:** Only one instance needed, global access
- **Example:** `Bank.get_instance()`

**2. Factory Pattern**
- **Where:** ResponseBuilder, CommandFactory
- **Why:** Creating different types of responses/commands
- **Example:** `ResponseBuilder.create_success(command, data)`

**3. Strategy Pattern**
- **Where:** Persistence (JSON vs SQLite vs CSV)
- **Why:** Interchangeable storage implementations
- **Example:** `IDataStore` interface with multiple implementations

**4. Repository Pattern**
- **Where:** AccountRepository
- **Why:** Abstraction over data access
- **Example:** `AccountRepository.get_by_number(account_number)`

**5. Command Pattern**
- **Where:** Protocol command handling
- **Why:** Encapsulate each command as object
- **Example:** `BCCommand.execute()`, `ACCommand.execute()`

### Recommended Patterns (Should Use):

**6. Observer Pattern**
- **Where:** Bank events (account created, transaction made)
- **Why:** Notify logger, persistence, statistics
- **Example:** `bank.subscribe(logger)`, `bank.notify_observers(event)`

**7. Facade Pattern**
- **Where:** BankFacade to simplify complex operations
- **Why:** Simplify interface for ClientHandler
- **Example:** `BankFacade.process_command(command_string)`

**8. Template Method Pattern**
- **Where:** Base command class with execute flow
- **Why:** Common command processing steps
- **Example:** `BaseCommand.execute()` → validate → process → log → respond

---

## 7. PROJECT STRUCTURE

```
bank_node/
├── main.py                          # Entry point
├── config.json                      # Configuration file
├── requirements.txt                 # Dependencies (if any)
├── README.md                        # Documentation
│
├── core/                            # BUSINESS LOGIC LAYER
│   ├── __init__.py
│   ├── bank_account.py             # Account model (Entity)
│   ├── bank.py                     # Bank manager (Singleton)
│   ├── account_repository.py       # Repository pattern
│   └── config_manager.py           # Configuration (Singleton)
│
├── network/                         # PRESENTATION LAYER
│   ├── __init__.py
│   ├── tcp_server.py               # TCP server (main listener)
│   ├── client_handler.py           # Thread per client
│   ├── proxy_client.py             # ESSENTIALS: outgoing
│   └── network_scanner.py          # HACKER: IP scanning
│
├── protocol/                        # PROTOCOL HANDLING
│   ├── __init__.py
│   ├── command_enum.py             # Enum of all commands
│   ├── command_parser.py           # Parse incoming strings
│   ├── command_factory.py          # Factory: create command objects
│   ├── commands/                   # Command Pattern
│   │   ├── __init__.py
│   │   ├── base_command.py         # Abstract base (Template Method)
│   │   ├── bc_command.py           # BC implementation
│   │   ├── ac_command.py           # AC implementation
│   │   ├── ad_command.py           # AD implementation
│   │   ├── aw_command.py           # AW implementation
│   │   ├── ab_command.py           # AB implementation
│   │   ├── ar_command.py           # AR implementation
│   │   ├── ba_command.py           # BA implementation
│   │   ├── bn_command.py           # BN implementation
│   │   └── rp_command.py           # RP implementation (HACKER)
│   ├── response_builder.py         # Factory: build responses
│   └── validator.py                # Validation logic
│
├── persistence/                     # DATA ACCESS LAYER
│   ├── __init__.py
│   ├── i_data_store.py             # Interface (Strategy)
│   ├── json_data_store.py          # JSON implementation
│   ├── sqlite_data_store.py        # SQLite implementation (bonus)
│   └── auto_saver.py               # Periodic auto-save
│
├── robbery/                         # HACKER LEVEL
│   ├── __init__.py
│   ├── bank_info.py                # DTO for bank data
│   ├── robbery_planner.py          # Main planner (Facade)
│   ├── greedy_strategy.py          # Greedy algorithm (Strategy)
│   └── dp_strategy.py              # DP algorithm (Strategy)
│
├── utils/                           # UTILITIES
│   ├── __init__.py
│   ├── logger.py                   # Centralized logging (Singleton)
│   ├── decorators.py               # @timeout, @log_execution
│   └── ip_helper.py                # IP validation, detection
│
└── tests/                           # UNIT TESTS
    ├── __init__.py
    ├── test_protocol.py
    ├── test_bank.py
    ├── test_commands.py
    └── test_network.py
```

---

## 8. DETAILED COMPONENT COMMUNICATION DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL CLIENTS                                │
│                  (PuTTY, Telnet, Other Bank Nodes)                      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ TCP Connection
                             │ (Port 65525-65535)
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                      TcpServer                                  │    │
│  │  - Listens on configured port                                  │    │
│  │  - Accepts incoming connections                                │    │
│  │  - Creates thread for each client                              │    │
│  │  - Uses ThreadPoolExecutor (Object Pool Pattern)               │    │
│  └──────────┬──────────────────────────────────────────────────────┘   │
│             │ spawns thread                                             │
│             ▼                                                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │              ClientHandler (Thread per client)                  │    │
│  │  - Receives raw data from socket                               │    │
│  │  - Manages client timeout                                      │    │
│  │  - Sends responses back                                        │    │
│  │  - Handles connection lifecycle                                │    │
│  └──────────┬──────────────────────────────────────────────────────┘   │
│             │ sends raw command string                                  │
└─────────────┼─────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PROTOCOL LAYER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    CommandParser                                │    │
│  │  - Parses raw string: "AD 10001/10.1.2.3 5000"                │    │
│  │  - Extracts: command code, account, IP, amount                 │    │
│  │  - Returns parsed data                                         │    │
│  └──────────┬──────────────────────────────────────────────────────┘   │
│             │ parsed data                                               │
│             ▼                                                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    Validator                                    │    │
│  │  - Validates account number (10000-99999)                      │    │
│  │  - Validates IP format                                         │    │
│  │  - Validates amount (>= 0)                                     │    │
│  │  - Returns validation result                                   │    │
│  └──────────┬──────────────────────────────────────────────────────┘   │
│             │ if valid                                                  │
│             ▼                                                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │              CommandFactory (Factory Pattern)                   │    │
│  │  - Creates appropriate Command object                          │    │
│  │  - BC → BCCommand                                              │    │
│  │  - AC → ACCommand                                              │    │
│  │  - AD → ADCommand, etc.                                        │    │
│  └──────────┬──────────────────────────────────────────────────────┘   │
│             │ returns Command object                                    │
│             ▼                                                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │          Specific Command (Command Pattern)                     │    │
│  │  ┌──────────────────────────────────────────────────────────┐  │    │
│  │  │ BaseCommand (Template Method)                            │  │    │
│  │  │  1. validate()   ◄─── implemented by subclass           │  │    │
│  │  │  2. execute()    ◄─── implemented by subclass           │  │    │
│  │  │  3. log()        ◄─── common for all                    │  │    │
│  │  └──────────────────────────────────────────────────────────┘  │    │
│  │  ┌──────────────────────────────────────────────────────────┐  │    │
│  │  │ BCCommand, ACCommand, ADCommand, etc.                    │  │    │
│  │  │  - Each implements specific logic                        │  │    │
│  │  └──────────────────────────────────────────────────────────┘  │    │
│  └──────────┬──────────────────────────────────────────────────────┘   │
│             │ calls business logic                                      │
└─────────────┼─────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │          Bank (Singleton Pattern)                               │    │
│  │  - Manages all accounts                                        │    │
│  │  - Thread-safe operations (Lock)                               │    │
│  │  - Notifies observers on events (Observer Pattern)             │    │
│  │                                                                 │    │
│  │  Methods:                                                       │    │
│  │  - create_account() → generates unique number                  │    │
│  │  - get_account(number) → retrieves account                     │    │
│  │  - get_total_amount() → sum of all balances                    │    │
│  │  - get_client_count() → count of accounts                      │    │
│  └──────────┬───────────────────────────┬──────────────────────────┘   │
│             │ delegates to              │ notifies                      │
│             ▼                            ▼                               │
│  ┌─────────────────────────┐  ┌────────────────────────────────┐       │
│  │  AccountRepository      │  │   Observers (Observer Pattern)  │       │
│  │  (Repository Pattern)   │  │   - Logger                      │       │
│  │  - CRUD operations      │  │   - AutoSaver                   │       │
│  │  - Data abstraction     │  │   - StatisticsCollector         │       │
│  └──────────┬──────────────┘  └────────────────────────────────┘       │
│             │ uses                                                       │
│             ▼                                                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    BankAccount (Entity)                         │    │
│  │  - number: int (10000-99999)                                   │    │
│  │  - balance: int (>= 0)                                         │    │
│  │                                                                 │    │
│  │  Methods:                                                       │    │
│  │  - deposit(amount) → increases balance                         │    │
│  │  - withdraw(amount) → decreases balance or fails               │    │
│  │  - can_delete() → checks if balance == 0                       │    │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ saves/loads data
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       DATA ACCESS LAYER                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │      IDataStore (Strategy Pattern - Interface)                  │    │
│  │  - save(bank_code, accounts)                                   │    │
│  │  - load() → (bank_code, accounts)                              │    │
│  └──────────┬───────────────────────────┬──────────────────────────┘   │
│             │ implemented by            │ implemented by                │
│             ▼                            ▼                               │
│  ┌─────────────────────────┐  ┌────────────────────────────────┐       │
│  │  JsonDataStore          │  │  SqliteDataStore               │       │
│  │  - Saves to JSON file   │  │  - Saves to SQLite DB          │

---
```


## 6. CONFIGURATION

### Required Configurable Parameters:
✅ Port (65525-65535)
✅ IP address (if not detected dynamically)
✅ Response timeout (default 5s)
✅ Inactive client timeout (default e.g., 60s)
✅ For HACKER: IP range for scanning (default 10.1.2.1-254)


### Recommended Additional:
- Max concurrent clients
- Path to persistence file
- Logging level (DEBUG, INFO, ERROR)
- Auto-save interval

---

## 7. TIMEOUTS (CRITICAL!)

### Response Timeout (default 5s)
- Applies to **all commands**
- If processing takes longer → `ER Request timeout.`

### Inactive Client Timeout
- If client sends nothing for X seconds → disconnect
- Log disconnection
- Free resources (socket, thread)

### Proxy Forwarding Timeout (ESSENTIALS)
- If foreign bank doesn't respond → `ER Target bank unavailable.`

### Network Scanning Timeout (HACKER)
- When scanning IPs: short timeout (1-2s)
- If IP doesn't respond quickly → no bank there, continue

---

## 8. LOGGING

### What must be in logs:

✅ All incoming connections (IP, time)
✅ All received commands
✅ All sent responses
✅ All errors (with details)
✅ State changes (account creation/deletion, transactions)
✅ Proxy forwarding (where, when, result)
✅ Network scanning (IP range, banks found)
✅ Client disconnections (normal and timeout)


### Log Format:


```
[2026-01-19 14:23:45] [INFO] Client connected: 10.1.2.15:51234
[2026-01-19 14:23:46] [INFO] Received: AC
[2026-01-19 14:23:46] [INFO] Created account: 10001
[2026-01-19 14:23:46] [INFO] Sent: AC 10001/10.1.2.3
```

---


## 9. DATA PERSISTENCE

### What must survive restart:
- ✅ All accounts (account numbers)
- ✅ All balances
- ✅ Configuration

### When to save:
- **Option A:** After each change (safe but slow)
- **Option B:** Periodically (e.g., every 30s)
- **Option C:** On graceful shutdown + periodically
- **Best:** B or C with transaction log

### Python Technologies:

**JSON (recommended for simplicity):**
```python
{
  "bank_code": "10.1.2.3",
  "accounts": [
    {"number": 10001, "balance": 5000},
    {"number": 10002, "balance": 12500}
  ]
}
```

**SQLite (recommended for professionalism):**
```python
import sqlite3

conn = sqlite3.connect('bank.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_number INTEGER PRIMARY KEY,
        balance INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
```

---


## 11. DOCUMENTATION (Required Items)

### Documentation Structure:

```markdown
# P2P Bank Node - Documentation

## 1. Running the Application
Exact procedure for starting (with examples)

## 2. Configuration
All configurable parameters

## 3. Usage
How to use (PuTTY examples)

## 4. Architecture
Description of structure, classes, design patterns

## 5. Reused Code ⭐
List of code from previous projects with links

## 6. Sources Used ⭐
- Python documentation
- Stack Overflow (specific links)
- ChatGPT: [link to chat](...)
- Books, tutorials

## 7. Testing
How you tested, with whom, results

## 8. Known Issues / Limitations
What doesn't work ideally and why
```


## 12. CHECKLIST BEFORE SUBMISSION

### Functionality:
- [ ] All commands work (BC, AC, AD, AW, AB, AR, BA, BN)
- [ ] RP command works (HACKER)
- [ ] Proxy forwarding works (ESSENTIALS/HACKER)
- [ ] Correct response format (watch AD/AW/AR!)
- [ ] Persistence works (restart = data OK)
- [ ] Timeouts work (responses and inactive clients)

### Technical:
- [ ] Runs on school PC without IDE
- [ ] Port 65525-65535
- [ ] UTF-8 encoding
- [ ] True parallelization (multi-threading)
-

