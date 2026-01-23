import random
import threading
from typing import Optional, List, Any
from bank_node.core.config_manager import ConfigManager
from bank_node.core.account_repository import AccountRepository
from bank_node.core.bank_account import BankAccount

class Bank:
    """
    Singleton class acting as the Facade for all banking operations.
    Manages accounts via AccountRepository and uses ConfigManager for configuration.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Bank, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, account_repository: Optional[AccountRepository] = None):
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
        """Sets the account repository if not provided during init."""
        self.account_repository = repository

    def subscribe(self, observer: Any):
        """Adds an observer to the list."""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def unsubscribe(self, observer: Any):
        """Removes an observer from the list."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    def notify(self, event_type: str, data: Any = None):
        """Notifies all observers of an event."""
        observers_copy = self._observers[:] 
        for observer in observers_copy:
            observer.update(event_type, data)

    def create_account(self) -> int:
        """
        Generates a unique 5-digit account number (10000-99999), 
        creates a BankAccount, adds it to the repository, and returns the number.
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
        """Returns the balance of the specified account."""
        account = self._get_account_or_raise(account_number)
        return account.balance

    def deposit(self, account_number: int, amount: int) -> int:
        """Deposits amount into the specified account. Returns new balance."""
        with self._lock:
            account = self._get_account_or_raise(account_number)
            new_balance = account.deposit(amount)
            # if self.account_repository:
            #     self.account_repository.save()
            self.notify("transaction", {"type": "deposit", "account": account_number, "amount": amount})
            return new_balance

    def withdraw(self, account_number: int, amount: int) -> int:
        """Withdraws amount from the specified account. Returns new balance."""
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
        Raises ValueError if account has non-zero balance.
        """
        with self._lock:
            account = self._get_account_or_raise(account_number)
            if account.balance > 0:
                raise ValueError("Cannot delete account with funds.")
            
            self.account_repository.remove_account(account_number)
            self.notify("account_removed", {"account_number": account_number})

    def get_total_capital(self) -> int:
        """Sums all account balances."""
        if not self.account_repository:
            return 0
        accounts = self.account_repository.get_all_accounts()
        return sum(acc.balance for acc in accounts)

    def get_client_count(self) -> int:
        """Returns the number of clients (accounts)."""
        if not self.account_repository:
            return 0
        return len(self.account_repository.get_all_accounts())

    def _get_account_or_raise(self, account_number: int) -> BankAccount:
        """Helper to retrieve account or raise error if not found."""
        if not self.account_repository:
            raise RuntimeError("Account repository not initialized.")
        
        account = self.account_repository.get_account(account_number)
        if not account:
            raise ValueError(f"Account {account_number} not found.")
        return account
