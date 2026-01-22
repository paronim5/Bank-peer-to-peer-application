import json
import os
from typing import Any, Dict, Optional

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.config = {}
        return cls._instance

    def load_config(self, path: str = 'config.json') -> None:
        """
        Loads configuration from a JSON file.
        If the file is not found, it falls back to hardcoded defaults.
        """
        if not os.path.exists(path):
            # Fallback defaults
            self.config = {
                "server": {
                    "ip": "127.0.0.1",
                    "port": 65525
                },
                "persistence": {
                    "type": "json",
                    "file_path": "bank_data.json"
                },
                "logging": {
                    "level": "INFO",
                    "file": "bank_node.log"
                }
            }
            print(f"Warning: Config file '{path}' not found. Loaded defaults.")
            return

        try:
            with open(path, 'r') as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Critical Error: Failed to decode JSON from '{path}': {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value by key.
        """
        return self.config.get(key, default)
