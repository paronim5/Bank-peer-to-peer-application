import json
import os

class ConfigManager:
    """
    Singleton class for managing application configuration.
    Loads settings from config.json.
    """
    _instance = None
    _config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self, path="bank_node/config.json"):
        """Loads configuration from the JSON file."""
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
        """Retrieves a configuration value by key."""
        return self._config.get(key, default)
