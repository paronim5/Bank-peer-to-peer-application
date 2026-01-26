from typing import Any
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.network.network_scanner import NetworkScanner
from bank_node.robbery.greedy_strategy import GreedyStrategy
from bank_node.utils.ip_helper import get_primary_local_ip, get_local_subnet_range

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
        network_config = self.bank.config_manager.get("network", {})
        
        ip_range_start = network_config.get("scan_start")
        ip_range_end = network_config.get("scan_end")
        
        if not ip_range_start or not ip_range_end:
            # Auto-detect subnet
            current_ip = get_primary_local_ip()
            ip_range_start, ip_range_end = get_local_subnet_range(current_ip)
            
        scan_port = self.bank.config_manager.get("server", {}).get("port", 65525)
        scanner_timeout = network_config.get("scanner_timeout", 2)
        
        # Initialize Scanner
        scanner = NetworkScanner(port=scan_port, timeout=scanner_timeout)
        
        # Scan
        # Note: This is a blocking operation and might take time.
        active_banks = scanner.scan(ip_range_start, ip_range_end)
        
        # Plan
        strategy = GreedyStrategy()
        selected_banks, total_stolen, total_clients = strategy.plan(active_banks, target_amount)
        
        # Format Response
        if not selected_banks:
            return f"RP To achieve {target_amount}, no suitable banks found in range {ip_range_start}-{ip_range_end}."
            
        bank_ips = " and ".join([b.ip for b in selected_banks])
        return f"RP To achieve {target_amount}, rob banks {bank_ips}, affecting only {total_clients} clients (Total: {total_stolen})."
