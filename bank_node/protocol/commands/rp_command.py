from typing import Any
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.network.network_scanner import NetworkScanner
from bank_node.robbery.greedy_strategy import GreedyStrategy

class RPCommand(BaseCommand):
    """
    Implements the RP (Robbery Plan) command.
    Scans the network and plans a robbery.
    """

    def validate_args(self) -> None:
        """
        Validates the arguments for RP command.
        Expects 1 arg: `target_amount` (integer).
        """
        if len(self.args) != 1:
            raise ValueError("Invalid arguments count. Usage: RP <target_amount>")
        
        amount_str = self.args[0]
        if not amount_str.isdigit():
            raise ValueError("Target amount must be a positive integer")

    def execute_logic(self) -> Any:
        """
        Scans network and calculates robbery plan.
        Returns: "RP <message>"
        """
        target_amount = int(self.args[0])
        
        # Determine scan range
        # For this implementation, we'll scan a small range around the local IP or a config range.
        # Ideally, this should be configurable. 
        # Let's check if config has network range, otherwise default to local subnet range.
        
        network_config = self.bank.config_manager.get("network", {})
        ip_range_start = network_config.get("scan_start", "127.0.0.1")
        ip_range_end = network_config.get("scan_end", "127.0.0.5") # Default small range for testing
        scan_port = self.bank.config_manager.get("server", {}).get("port", 65525)
        
        # Initialize Scanner
        scanner = NetworkScanner(port=scan_port, timeout=1) # Fast timeout for scanning
        
        # Scan
        # Note: This is a blocking operation and might take time.
        # In a real async server, this should be offloaded. 
        # But here our BaseCommand executes synchronously in the ClientHandler thread.
        active_banks = scanner.scan(ip_range_start, ip_range_end)
        
        # Plan
        strategy = GreedyStrategy()
        selected_banks, total_stolen, total_clients = strategy.plan(active_banks, target_amount)
        
        # Format Response
        if not selected_banks:
            return f"RP To achieve {target_amount}, no suitable banks found in range {ip_range_start}-{ip_range_end}."
            
        bank_ips = " and ".join([b.ip for b in selected_banks])
        return f"RP To achieve {target_amount}, rob banks {bank_ips}, affecting only {total_clients} clients (Total: {total_stolen})."
