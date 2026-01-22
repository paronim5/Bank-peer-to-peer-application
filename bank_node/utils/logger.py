import logging
import sys
import os
from core.config_manager import ConfigManager

class Logger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.logger = logging.getLogger("BankNode")
        self.logger.propagate = False  # Prevent propagation to root logger to avoid duplicates
        
        # Ensure ConfigManager is loaded
        config_manager = ConfigManager()
        if not config_manager.get("logging"):
             config_manager.load_config()
             
        log_config = config_manager.get("logging", {})
        
        # Determine Log Level
        level_str = log_config.get("level", "INFO").upper()
        level = getattr(logging, level_str, logging.INFO)
        self.logger.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Stream Handler (Console)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        
        # File Handler
        file_path = log_config.get("file", "bank_node.log")
        # Ensure directory exists if path contains directories
        log_dir = os.path.dirname(file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)
