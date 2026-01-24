import sqlite3
import json
from typing import Dict, Any
from bank_node.persistence.i_data_store import IDataStore

class SqliteDataStore(IDataStore):
    """
    Implementation of IDataStore using SQLite for persistence.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """
        Creates the necessary tables if they don't exist.
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
        Clears the existing table and re-inserts current state to ensure consistency.
        
        Args:
            data (dict): The data to save. Structure: {account_id: account_dict}
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
        
        Returns:
            dict: The loaded data. Structure: {account_id: account_dict}
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
