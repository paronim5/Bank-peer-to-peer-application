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
        Saves the entire bank state.
        
        Args:
            data (dict): The data to save. Expected structure: {'accounts': {...}}
        """
        pass

    @abstractmethod
    def load_data(self) -> Dict[str, Any]:
        """
        Loads the bank state.
        
        Returns:
            dict: The loaded data. Expected structure: {'accounts': {...}}
        """
        pass
