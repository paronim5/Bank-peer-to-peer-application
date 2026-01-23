from typing import List, Tuple
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.network.network_scanner import NetworkScanner
from robbery.dp_strategy import DpStrategy
from robbery.greedy_strategy import GreedyStrategy
from bank_node.core.config_manager import ConfigManager

class RPCommand(BaseCommand):
    """
    Implements the Robbery Plan (RP) command.
    Scans the network for banks and plans a robbery to achieve the target amount.
    """

    def validate_args(self) -> bool:
        """
        Validates the arguments. Expects exactly one argument: target_amount.
        """
        if len(self.args) != 1:
            return False
        try:
            amount = int(self.args[0])
            if amount <= 0:
                return False
        except ValueError:
            return False
        return True

    def execute_logic(self) -> str:
        """
        Executes the robbery planning logic.
        """
        target_amount = int(self.args[0])
        
        # Get configuration
        config = ConfigManager()
        # Default scan range (could be configured)
        scan_start_ip = config.get("scan_start_ip", "127.0.0.1")
        scan_end_ip = config.get("scan_end_ip", "127.0.0.1")
        scan_port = config.get("server", {}).get("port", 65525)
        
        # Instantiate Scanner
        scanner = NetworkScanner(port=scan_port)
        
        # Scan network
        # For the purpose of this command, we scan the configured range.
        # If running locally with ports, this might only find self or nothing if ports differ.
        # But we follow the architecture provided.
        discovered_banks = scanner.scan(scan_start_ip, scan_end_ip)
        
        # Choose Strategy
        strategy_type = config.get("robbery_strategy", "dp").lower()
        if strategy_type == "greedy":
            strategy = GreedyStrategy()
        else:
            strategy = DpStrategy()
            
        # Plan robbery
        selected_banks, total_stolen, total_clients = strategy.plan(discovered_banks, target_amount)
        
        # Format response
        if not selected_banks:
            return f"RP To achieve {target_amount}, no plan could be formed."
            
        bank_ips = [bank.ip for bank in selected_banks]
        
        # "rob banks A and B"
        if len(bank_ips) == 1:
            banks_str = f"bank {bank_ips[0]}"
        else:
            banks_str = f"banks {' and '.join(bank_ips)}"
            
        return f"RP To achieve {target_amount}, rob {banks_str}, affecting {total_clients} clients."
