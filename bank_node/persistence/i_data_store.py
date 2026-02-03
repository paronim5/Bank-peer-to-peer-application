from abc import ABC, abstractmethod
from typing import Dict, Any

class IDataStore(ABC):
    """
    Abstract Base Class for Data Storage Strategy.
    Defines the contract for saving and loading bank data.
    """

    @abstractmethod
    def save_data(self, data: Dict[str, Any]) -> None:
        """
        Saves the entire bank state to the persistent storage.
        
        This method is responsible for persisting the current state of the bank,
        including all accounts and their transaction histories.
        
        Args:
            data (Dict[str, Any]): A dictionary containing the data to save.
                Expected structure: {'accounts': {account_id: account_data, ...}}
        
        Raises:
            IOError: If the data cannot be written to the storage medium.
            Exception: For any underlying storage errors.
            
        Side Effects:
            - Writes data to the configured storage medium (file, database, etc.).
            - May overwrite existing data.
        """
        pass

    @abstractmethod
    def load_data(self) -> Dict[str, Any]:
        """
        Loads the bank state from the persistent storage.
        
        This method retrieves the saved state of the bank. If no data exists,
        it should return an empty dictionary or a default structure.
        
        Returns:
            Dict[str, Any]: A dictionary containing the loaded data.
                Expected structure: {'accounts': {account_id: account_data, ...}}
                Returns an empty dictionary if no data is found.
        
        Raises:
            IOError: If the data cannot be read from the storage medium.
            Exception: For any underlying storage errors.
            
        Side Effects:
            - Reads data from the configured storage medium.
        """
        pass
