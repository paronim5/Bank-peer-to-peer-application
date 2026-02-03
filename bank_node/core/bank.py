import random
import threading
from typing import Optional, List, Any
from bank_node.core.config_manager import ConfigManager
from bank_node.core.account_repository import AccountRepository
from bank_node.core.bank_account import BankAccount

class Bank:
    """
    Singleton class acting as the Facade for all banking operations.
    Manages accounts via AccountRepository, handles configuration, and provides
    a unified interface for transactions and account management. Implements
    the Observer pattern for event notifications.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance of the Bank class exists (Singleton Pattern).
        """
        if cls._instance is None:
            cls._instance = super(Bank, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, account_repository: Optional[AccountRepository] = None):
        """
        Initialize the Bank singleton.

        Args:
            account_repository (Optional[AccountRepository]): The repository for account management.
                Can be injected for testing purposes.
        """
        if self._initialized:
            return
        
        self.config_manager = ConfigManager()
        self._lock = threading.RLock()
        self._observers: List[Any] = []
        # In a real app, repo might be injected or created here based on config.
        # For this step, we allow injection for easier testing, or assume it's set later.
        self.account_repository = account_repository
        self._initialized = True

    def set_repository(self, repository: AccountRepository):
        """
        Sets the account repository if not provided during init.

        Args:
            repository (AccountRepository): The repository instance to use.
        """
        self.account_repository = repository

    def subscribe(self, observer: Any):
        """
        Adds an observer to the list for event notifications.

        Args:
            observer (Any): The observer object (must implement `update(event_type, data)`).
        """
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def unsubscribe(self, observer: Any):
        """
        Removes an observer from the list.

        Args:
            observer (Any): The observer object to remove.
        """
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    def notify(self, event_type: str, data: Any = None):
        """
        Notifies all observers of an event.

        Args:
            event_type (str): The type/name of the event (e.g., "transaction", "account_created").
            data (Any, optional): Additional data associated with the event.
        """
        observers_copy = self._observers[:] 
        for observer in observers_copy:
            observer.update(event_type, data)

    def create_account(self) -> int:
        """
        Generates a unique 5-digit account number and creates a new BankAccount.

        Returns:
            int: The unique account number of the created account.

        Raises:
            RuntimeError: If the account repository is not initialized.
            
        Side Effects:
            Adds the new account to the repository and notifies observers.
        """
        with self._lock:
            if not self.account_repository:
                raise RuntimeError("Account repository not initialized.")

            # Try generating a unique number
            while True:
                number = random.randint(10000, 99999)
                if self.account_repository.get_account(number) is None:
                    break
            
            # Default balance 0
            account = BankAccount(number, 0)
            self.account_repository.add_account(account)
            # self.account_repository.save() # Removed in favor of Observer
            self.notify("account_created", {"account_number": number})
            return number

    def get_balance(self, account_number: int) -> int:
        """
        Returns the balance of the specified account.

        Args:
            account_number (int): The account number to check.

        Returns:
            int: The current balance of the account.

        Raises:
            ValueError: If the account does not exist.
            RuntimeError: If the repository is not initialized.
        """
        account = self._get_account_or_raise(account_number)
        return account.balance

    def deposit(self, account_number: int, amount: int) -> int:
        """
        Deposits amount into the specified account.

        Args:
            account_number (int): The target account number.
            amount (int): The amount to deposit (must be positive).

        Returns:
            int: The new balance of the account.

        Raises:
            ValueError: If the account doesn't exist or amount is invalid.
            RuntimeError: If the repository is not initialized.

        Side Effects:
            Updates account balance and notifies observers of the transaction.
        """
        with self._lock:
            account = self._get_account_or_raise(account_number)
            new_balance = account.deposit(amount)
            # if self.account_repository:
            #     self.account_repository.save()
            self.notify("transaction", {"type": "deposit", "account": account_number, "amount": amount})
            return new_balance

    def withdraw(self, account_number: int, amount: int) -> int:
        """
        Withdraws amount from the specified account.

        Args:
            account_number (int): The target account number.
            amount (int): The amount to withdraw (must be positive).

        Returns:
            int: The new balance of the account.

        Raises:
            ValueError: If account missing, amount invalid, or insufficient funds.
            RuntimeError: If the repository is not initialized.

        Side Effects:
            Updates account balance and notifies observers of the transaction.
        """
        with self._lock:
            account = self._get_account_or_raise(account_number)
            new_balance = account.withdraw(amount)
            # if self.account_repository:
            #     self.account_repository.save()
            self.notify("transaction", {"type": "withdraw", "account": account_number, "amount": amount})
            return new_balance

    def remove_account(self, account_number: int) -> None:
        """
        Removes the specified account.

        Args:
            account_number (int): The account number to remove.

        Raises:
            ValueError: If the account does not exist or has a non-zero balance.
            RuntimeError: If the repository is not initialized.

        Side Effects:
            Removes the account from the repository and notifies observers.
        """
        with self._lock:
            account = self._get_account_or_raise(account_number)
            if account.balance > 0:
                raise ValueError("Cannot delete account with funds.")
            
            self.account_repository.remove_account(account_number)
            self.notify("account_removed", {"account_number": account_number})

    def get_total_capital(self) -> int:
        """
        Sums all account balances to calculate the bank's total capital.

        Returns:
            int: The sum of balances of all accounts.
        """
        if not self.account_repository:
            return 0
        accounts = self.account_repository.get_all_accounts()
        return sum(acc.balance for acc in accounts)

    def get_client_count(self) -> int:
        """
        Returns the total number of clients (accounts).

        Returns:
            int: The count of active accounts.
        """
        if not self.account_repository:
            return 0
        return len(self.account_repository.get_all_accounts())

    def _get_account_or_raise(self, account_number: int) -> BankAccount:
        """
        Helper to retrieve an account or raise an error if not found.

        Args:
            account_number (int): The account number to look up.

        Returns:
            BankAccount: The account object.

        Raises:
            ValueError: If the account is not found.
            RuntimeError: If the repository is not initialized.
        """
        if not self.account_repository:
            raise RuntimeError("Account repository not initialized.")
        
        account = self.account_repository.get_account(account_number)
        if not account:
            raise ValueError(f"Account {account_number} not found.")
        return account
