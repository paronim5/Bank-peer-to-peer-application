import sys
import os
import argparse
import time
import threading

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bank_node.core.bank import Bank
from bank_node.network.tcp_server import TcpServer
from bank_node.core.config_manager import ConfigManager
from bank_node.core.account_repository import AccountRepository
from bank_node.persistence.json_data_store import JsonDataStore

def run_node(port, data_dir):
    # Setup ConfigManager manually
    config = ConfigManager()
    config._config = {
        "server": {"ip": "127.0.0.1", "port": port},
        "persistence": {"type": "json", "file_path": os.path.join(data_dir, "bank_data.json")},
        "logging": {"level": "INFO", "file": os.path.join(data_dir, "bank_node.log")}
    }
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Initialize Persistence
    data_store = JsonDataStore(os.path.join(data_dir, "bank_data.json"))
    repository = AccountRepository(data_store)
    
    # Initialize Bank (Singleton)
    # Since we are in a separate process, this is the only Bank instance.
    bank = Bank()
    # Force re-initialization of repo in case it was already set (though in new process it won't be)
    bank.set_repository(repository)
    
    # Start Server
    server = TcpServer("127.0.0.1", port)
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--data-dir", type=str, required=True)
    args = parser.parse_args()
    
    run_node(args.port, args.data_dir)
