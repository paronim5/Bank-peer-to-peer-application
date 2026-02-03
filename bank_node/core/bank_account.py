import threading

class BankAccount:
    """
    Represents a bank account with thread-safe balance operations.
    Encapsulates account data and ensures data integrity during concurrent access.
    """
    def __init__(self, number: int, balance: int = 0):
        """
        Initialize a new BankAccount instance.

        Args:
            number (int): The unique account number (must be 5 digits, 10000-99999).
            balance (int, optional): Initial account balance. Defaults to 0.

        Raises:
            ValueError: If the account number is invalid.
        """
        self._validate_account_number(number)
        self.number = number
        self.balance = balance
        self.lock = threading.Lock()

    def _validate_account_number(self, number: int):
        """
        Validates that the account number is a 5-digit integer.

        Args:
            number (int): The account number to validate.

        Raises:
            ValueError: If the number is not between 10000 and 99999.
        """
        if not (10000 <= number <= 99999):
            raise ValueError(f"Invalid account number: {number}. Must be between 10000 and 99999.")

    def deposit(self, amount: int) -> int:
        """
        Deposits the given amount into the account in a thread-safe manner.
        
        Args:
            amount (int): The amount to deposit. Must be positive.
            
        Returns:
            int: The new balance after the deposit.
            
        Raises:
            ValueError: If the amount is not positive.

        Example:
            >>> account.deposit(100)
            100
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        with self.lock:
            self.balance += amount
            return self.balance

    def withdraw(self, amount: int) -> int:
        """
        Withdraws the given amount from the account in a thread-safe manner.
        
        Args:
            amount (int): The amount to withdraw. Must be positive.
            
        Returns:
            int: The new balance after the withdrawal.
            
        Raises:
            ValueError: If the amount is not positive or funds are insufficient.

        Example:
            >>> account.withdraw(50)
            50
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
        Serializes the bank account state to a dictionary.
        Useful for persistence.

        Returns:
            dict: A dictionary containing 'number' and 'balance'.

        Example:
            >>> account.to_dict()
            {'number': 12345, 'balance': 100}
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
        Factory method to create an instance from stored data.

        Args:
            data (dict): A dictionary containing 'number' and optionally 'balance'.

        Returns:
            BankAccount: A new BankAccount instance.

        Raises:
            ValueError: If 'number' is missing in the data.

        Example:
            >>> BankAccount.from_dict({'number': 12345, 'balance': 100})
            <BankAccount object>
        """
        if "number" not in data:
            raise ValueError("Missing 'number' in account data.")
        
        # balance defaults to 0 if missing, which fits our init logic
        return BankAccount(
            number=data["number"],
            balance=data.get("balance", 0)
        )
