import json
import os

class ConfigManager:
    """
    Singleton class for managing application configuration.
    Responsible for loading settings from config.json and providing access to them.
    """
    _instance = None
    _config = {}

    def __new__(cls):
        """
        Creates or returns the singleton instance of ConfigManager.
        Automatically loads configuration on first instantiation.

        Returns:
            ConfigManager: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self, path="bank_node/config.json"):
        """
        Loads configuration from the specified JSON file.
        Falls back to default settings if the file is missing or invalid.

        Args:
            path (str, optional): Path to the configuration file. Defaults to "bank_node/config.json".

        Side Effects:
            Updates the internal `_config` dictionary.

        Notes:
            Attempts to locate 'config.json' in the current directory if the provided path fails.
        """
        # Adjust path if running from root or subfolder
        if not os.path.exists(path):
            # Try looking in current directory
            if os.path.exists("config.json"):
                path = "config.json"
            else:
                 # Default fallback if file missing
                self._config = {
                    "server": {"ip": "127.0.0.1", "port": 65525},
                    "persistence": {"type": "json", "file_path": "bank_data.json"},
                    "logging": {"level": "INFO", "file": "bank_node.log"}
                }
                return

        try:
            with open(path, 'r') as f:
                self._config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback defaults
            self._config = {
                "server": {"ip": "127.0.0.1", "port": 65525},
                "persistence": {"type": "json", "file_path": "bank_data.json"},
                "logging": {"level": "INFO", "file": "bank_node.log"}
            }

    def get(self, key, default=None):
        """
        Retrieves a configuration value by key.

        Args:
            key (str): The configuration key to retrieve.
            default (Any, optional): The value to return if the key is not found. Defaults to None.

        Returns:
            Any: The configuration value or the default.

        Example:
            >>> config.get("server")
            {'ip': '127.0.0.1', 'port': 65525}
        """
        return self._config.get(key, default)
