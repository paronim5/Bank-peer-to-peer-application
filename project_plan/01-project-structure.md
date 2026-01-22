# Step 1: Project Structure & Environment Setup

## 1. Objective
Initialize the project repository with the required directory structure, establish the virtual environment, and create basic configuration files. This sets the foundation for a clean, layered architecture.

## 2. Technical Scope
- **Root Directory:** `bank_node/`
- **Subdirectories:** `core/`, `network/`, `protocol/`, `persistence/`, `robbery/`, `utils/`, `tests/`
- **Files:** `main.py` (empty), `config.json` (default), `requirements.txt`, `.gitignore`

## 3. Implementation Instructions
1.  Create the main project folder `bank_node` (if not already acting as root).
2.  Create the following directory tree:
    ```
    ├── core/
    ├── network/
    ├── protocol/
    │   └── commands/
    ├── persistence/
    ├── robbery/
    ├── utils/
    └── tests/
    ```
3.  Add `__init__.py` to all subdirectories to make them Python packages.
4.  Create a `config.ini` file in the root with default values:
    ```txt
    {
        "server": {
            "ip": "127.0.0.1",
            "port": 65525
        },
        "persistence": {
            "type": "json",
            "file_path": "bank_data.json"
        },
        "logging": {
            "level": "INFO",
            "file": "bank_node.log"
        }
    }
    ```
5.  Create a `.gitignore` file excluding `__pycache__`, `*.log`, `*.db`, and `bank_data.json`.

## 4. Dependencies
- None.

## 5. Validation Criteria
- Run `tree` (or `ls -R`) to verify the structure matches the specification.
- `config.json` contains valid JSON.
- Python can import packages from these directories (e.g., `import core`).

## 6. Expected Output/Deliverable
- A fully structured project directory ready for code implementation.
