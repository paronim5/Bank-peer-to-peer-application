import json
import os
from bank_node.persistence.i_data_store import IDataStore

class JsonDataStore(IDataStore):
    """
    Implementation of IDataStore using JSON files for persistence.
    """
    def __init__(self, file_path: str):
        """
        Initialize the JsonDataStore with a file path.

        Args:
            file_path (str): The absolute or relative path to the JSON file
                used for data storage.
        """
        self.file_path = file_path

    def save_data(self, data: dict):
        """
        Saves the dictionary data to the JSON file.

        This method serializes the provided data dictionary to JSON format
        and writes it to the specified file path. It creates the directory
        structure if it does not exist.

        Args:
            data (dict): The data to save.
        
        Raises:
            IOError: If the file cannot be opened or written to.
            
        Side Effects:
            - Creates directories if they don't exist.
            - Overwrites the content of the JSON file.
        """
        try:
            # Ensure directory exists
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving data to {self.file_path}: {e}")
            raise e

    def load_data(self) -> dict:
        """
        Loads data from the JSON file.

        Reads the JSON file and deserializes it into a dictionary.
        If the file does not exist or contains invalid JSON, returns an empty dictionary.

        Returns:
            dict: The loaded data as a dictionary. Returns {} if file is missing
            or JSON is invalid.

        Raises:
            IOError: If there is an error reading the file (other than file not found).
            
        Side Effects:
            - Opens and reads the file at `self.file_path`.
        """
        if not os.path.exists(self.file_path):
            return {}
        
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.file_path}")
            return {}
        except IOError as e:
            print(f"Error loading data from {self.file_path}: {e}")
            raise e
