from typing import Any
from bank_node.core.account_repository import AccountRepository

class AutoSaver:
    """
    Observer class that automatically saves the account repository
    whenever a relevant bank event occurs.
    """
    def __init__(self, account_repository: AccountRepository):
        """
        Initialize the AutoSaver.

        Args:
            account_repository (AccountRepository): The repository instance to save.
                This instance is used to trigger persistence when updates occur.
        """
        self.account_repository = account_repository

    def update(self, event_type: str, data: Any):
        """
        React to a notification from the subject (Bank).

        This method is the event handler for the Observer pattern.
        It triggers a save operation on the account repository.

        Args:
            event_type (str): The type of event that occurred (e.g., "transaction", "account_created").
            data (Any): Additional data associated with the event (e.g., the account object).
        
        Side Effects:
            - Calls `self.account_repository.save()`, which writes data to storage.
            - Prints a log message to stdout.
        """
        # For now, we save on every relevant event.
        # In a real system, we might check event_type or debounce.
        print(f"AutoSaver: Saving data due to event '{event_type}'")
        self.account_repository.save()
