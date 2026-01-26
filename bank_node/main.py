import sys
import os

# Add project root to sys.path to ensure 'bank_node' package is resolvable
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import logging
import time

# Add project root to sys.path to allow absolute imports when running directly
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from bank_node.core.config_manager import ConfigManager
from bank_node.core.bank import Bank
from bank_node.core.account_repository import AccountRepository
from bank_node.persistence.json_data_store import JsonDataStore
from bank_node.persistence.sqlite_data_store import SqliteDataStore
from bank_node.persistence.auto_saver import AutoSaver
from bank_node.network.tcp_server import TcpServer

def setup_logging(config: ConfigManager):
    """
    Configures the logging system based on configuration.
    """
    log_config = config.get("logging", {})
    level_str = log_config.get("level", "INFO").upper()
    file_path = log_config.get("file", "bank_node.log")
    
    level = getattr(logging, level_str, logging.INFO)
    
    # Configure root logger
    logging.basicConfig( 
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(file_path)
        ]
    )
    logging.info("Logging initialized.")

def main():
    """
    Main application entry point.
    """
    # 1. Load Configuration
    config_manager = ConfigManager()
    
    # 2. Initialize Logger
    setup_logging(config_manager)
    logger = logging.getLogger("Main")
    logger.info("Starting Bank Peer-to-Peer Node...")

    try:
        # 3. Initialize Persistence Layer
        persistence_config = config_manager.get("persistence", {})
        store_type = persistence_config.get("type", "json").lower()
        
        if store_type == "sqlite":
            db_path = persistence_config.get("file_path", "bank_data.db")
            data_store = SqliteDataStore(db_path)
            logger.info(f"Using SQLite persistence: {db_path}")
        else:
            db_path = persistence_config.get("file_path", "bank_data.json")
            data_store = JsonDataStore(db_path)
            logger.info(f"Using JSON persistence: {db_path}")

        account_repository = AccountRepository(data_store)
        
        # Load existing data
        logger.info(f"Loading data from {db_path}...")
        account_repository.load()
        logger.info(f"Loaded {len(account_repository.get_all_accounts())} accounts.")

        # 4. Initialize Bank (Facade)
        bank = Bank(account_repository)
        
        # 5. Initialize AutoSaver (Observer)
        auto_saver = AutoSaver(account_repository)
        bank.subscribe(auto_saver)
        logger.info("AutoSaver initialized and subscribed to Bank events.")

        # 6. Initialize TCP Server
        server_config = config_manager.get("server", {})
        host = server_config.get("ip", "127.0.0.1")
        port = server_config.get("port", 65525)
        
        server = TcpServer(host, port)
        
        # 7. Start Server
        logger.info(f"Starting TCP Server on {host}:{port}...")
        server.start()

    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt. Shutting down...")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
    finally:
        if 'server' in locals() and server.is_running:
            server.stop()
        logger.info("Application stopped.")

if __name__ == "__main__":
    main()
