from typing import Any
from bank_node.core.account_repository import AccountRepository

class AutoSaver:
    """
    Observer class that automatically saves the account repository
    whenever a relevant bank event occurs.
    """
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def update(self, event_type: str, data: Any):
        """
        Called when the subject (Bank) notifies of an event.
        
        Args:
            event_type (str): The type of event (e.g., "transaction", "account_created").
            data (Any): Additional data related to the event.
        """
        # For now, we save on every relevant event.
        # In a real system, we might check event_type or debounce.
        print(f"AutoSaver: Saving data due to event '{event_type}'")
        self.account_repository.save()
