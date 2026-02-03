import sqlite3
import json
from typing import Dict, Any
from bank_node.persistence.i_data_store import IDataStore

class SqliteDataStore(IDataStore):
    """
    Implementation of IDataStore using SQLite for persistence.
    """
    def __init__(self, db_path: str):
        """
        Initialize the SqliteDataStore with a database path.

        Automatically initializes the database schema if it doesn't exist.

        Args:
            db_path (str): The file path to the SQLite database.
        
        Side Effects:
            - Creates a new SQLite database file if one doesn't exist.
            - Calls `_initialize_db` to set up tables.
        """
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """
        Creates the necessary tables if they don't exist.

        Sets up the 'accounts' table with columns for account_id, balance, and history.

        Raises:
            sqlite3.Error: If the table creation fails.
            
        Side Effects:
            - Modifies the database schema.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id TEXT PRIMARY KEY,
                    balance INTEGER NOT NULL,
                    history TEXT
                )
            """)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error initializing database {self.db_path}: {e}")
            raise e

    def save_data(self, data: Dict[str, Any]) -> None:
        """
        Saves the entire bank state to SQLite.

        This implementation uses a "wipe and rewrite" strategy for simplicity:
        it clears the existing 'accounts' table and re-inserts the current state.
        This ensures the database exactly matches the in-memory state.
        Operations are performed within a transaction.

        Args:
            data (Dict[str, Any]): The data to save.
                Expected structure: {account_id: account_dict}

        Raises:
            sqlite3.Error: If the database operations fail.
            
        Side Effects:
            - Deletes all rows in the 'accounts' table.
            - Inserts new rows for the current data.
            - Commits the transaction to disk.
        """
        # Ensure tables exist (per requirements)
        self._initialize_db()
        
        accounts = data
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Use a transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Clear existing data to reflect current state (including deletions)
            cursor.execute("DELETE FROM accounts")
            
            # Insert current accounts
            for acc_id, acc_data in accounts.items():
                balance = acc_data.get('balance', 0)
                # Serialize history to JSON string
                history = json.dumps(acc_data.get('history', []))
                
                cursor.execute(
                    "INSERT INTO accounts (account_id, balance, history) VALUES (?, ?, ?)",
                    (acc_id, balance, history)
                )
            
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error saving data to {self.db_path}: {e}")
            raise e

    def load_data(self) -> Dict[str, Any]:
        """
        Loads the bank state from SQLite.

        Retrieves all rows from the 'accounts' table and reconstructs the
        dictionary structure expected by the application.
        Parses the JSON-serialized history field.

        Returns:
            Dict[str, Any]: The loaded data.
                Structure: {account_id: {'number': ..., 'balance': ..., 'history': ...}}
                Returns an empty dictionary if the table does not exist.

        Raises:
            sqlite3.Error: If the database query fails.
            
        Side Effects:
            - Connects to the SQLite database.
            - executes SELECT queries.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Access columns by name
            cursor = conn.cursor()
            
            # Check if table exists (in case file exists but empty or uninitialized)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")
            if not cursor.fetchone():
                conn.close()
                return {}

            cursor.execute("SELECT account_id, balance, history FROM accounts")
            rows = cursor.fetchall()
            
            accounts = {}
            for row in rows:
                acc_id = row['account_id']
                try:
                    history = json.loads(row['history'])
                except json.JSONDecodeError:
                    history = []
                
                # Ensure the structure matches what BankAccount.from_dict expects
                # BankAccount.from_dict expects 'number' and 'balance'
                accounts[acc_id] = {
                    'number': int(acc_id) if acc_id.isdigit() else acc_id,
                    'balance': row['balance'],
                    'history': history
                }
            
            conn.close()
            return accounts
            
        except sqlite3.Error as e:
            print(f"Error loading data from {self.db_path}: {e}")
            raise e
