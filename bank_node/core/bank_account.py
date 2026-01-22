import threading

class BankAccount:
    """
    Represents a bank account with thread-safe balance operations.
    """
    def __init__(self, number: int, balance: int = 0):
        self._validate_account_number(number)
        self.number = number
        self.balance = balance
        self.lock = threading.Lock()

    def _validate_account_number(self, number: int):
        """Validates that the account number is between 10000 and 99999."""
        if not (10000 <= number <= 99999):
            raise ValueError(f"Invalid account number: {number}. Must be between 10000 and 99999.")

    def deposit(self, amount: int) -> int:
        """
        Deposits the given amount into the account.
        
        Args:
            amount (int): The amount to deposit. Must be positive.
            
        Returns:
            int: The new balance.
            
        Raises:
            ValueError: If the amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        with self.lock:
            self.balance += amount
            return self.balance

    def withdraw(self, amount: int) -> int:
        """
        Withdraws the given amount from the account.
        
        Args:
            amount (int): The amount to withdraw. Must be positive.
            
        Returns:
            int: The new balance.
            
        Raises:
            ValueError: If the amount is not positive or funds are insufficient.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        with self.lock:
            if self.balance < amount:
                raise ValueError("Insufficient funds.")
            self.balance -= amount
            return self.balance

    def to_dict(self) -> dict:
        """
        Serializes the bank account to a dictionary.
        """
        with self.lock:
            return {
                "number": self.number,
                "balance": self.balance
            }

    @staticmethod
    def from_dict(data: dict) -> 'BankAccount':
        """
        Deserializes a bank account from a dictionary.
        """
        if "number" not in data:
            raise ValueError("Missing 'number' in account data.")
        
        # balance defaults to 0 if missing, which fits our init logic
        return BankAccount(
            number=data["number"],
            balance=data.get("balance", 0)
        )
