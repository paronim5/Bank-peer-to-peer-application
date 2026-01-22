from typing import Dict, List, Optional
from bank_node.core.bank_account import BankAccount
from bank_node.persistence.i_data_store import IDataStore

class AccountRepository:
    """
    Repository for managing BankAccount entities.
    Abstracts the data persistence layer using IDataStore.
    """
    def __init__(self, data_store: IDataStore):
        self._data_store = data_store
        self._accounts: Dict[int, BankAccount] = {}

    def add_account(self, account: BankAccount) -> None:
        """Adds an account to the repository."""
        self._accounts[account.number] = account

    def get_account(self, number: int) -> Optional[BankAccount]:
        """Retrieves an account by its number. Returns None if not found."""
        return self._accounts.get(number)

    def remove_account(self, number: int) -> None:
        """Removes an account from the repository."""
        if number in self._accounts:
            del self._accounts[number]

    def get_all_accounts(self) -> List[BankAccount]:
        """Returns a list of all accounts in the repository."""
        return list(self._accounts.values())

    def load(self) -> None:
        """
        Loads accounts from the data store.
        Populates the internal memory with BankAccount objects.
        """
        data = self._data_store.load_data()
        self._accounts.clear()
        
        # Expecting data to be a dictionary where keys are account numbers (str) and values are account data
        # or just a list/dict of accounts.
        # Based on BankAccount.to_dict, it returns {"number": ..., "balance": ...}
        # Let's assume the store saves a dict mapping account_number -> account_data for easy lookup,
        # or a list. Let's support a dictionary of accounts for O(1) access.
        
        # If the stored data is just the raw dictionary saved from save()
        for key, account_data in data.items():
            try:
                # The key in JSON might be a string, but account number is int
                # BankAccount.from_dict expects the dict to contain 'number'
                account = BankAccount.from_dict(account_data)
                self._accounts[account.number] = account
            except (ValueError, TypeError):
                # Skip invalid entries
                continue

    def save(self) -> None:
        """
        Saves all accounts to the data store.
        Converts BankAccount objects to dictionaries.
        """
        data = {}
        for number, account in self._accounts.items():
            data[str(number)] = account.to_dict()
        self._data_store.save_data(data)
