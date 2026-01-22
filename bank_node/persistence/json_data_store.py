import json
import os
from bank_node.persistence.i_data_store import IDataStore

class JsonDataStore(IDataStore):
    """
    Implementation of IDataStore using JSON files for persistence.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_data(self, data: dict):
        """
        Saves the dictionary data to the JSON file.
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
        Loads data from the JSON file. Returns empty dict if file doesn't exist.
        Handles JSON decode errors by returning empty dict.
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
