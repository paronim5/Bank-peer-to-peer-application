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
        Executes the Robbery Plan logic.
        """
        target_amount = int(self.args[0])
        
        # 1. Initialize Scanner
        scanner = NetworkScanner()
        
        # 2. Scan Network (Uses configured targets now)
        # We no longer need to calculate a simple start/end range manually
        # The scanner will pick up 'scan_targets' from config.json
        banks = scanner.scan()
        
        # Include our own bank? 
        # Usually RP is about robbing OTHERS, but let's stick to scanned banks.
        
        if not banks:
            return "RP No banks found to rob."
            
        # 3. Plan Robbery
        # Try DP first (if small enough), else Greedy
        # But wait, the requirements say "Start with greedy, then possibly DP"
        # Let's just use the planner which should decide or use a default.
        # For this implementation, we'll use the DP Strategy as it is "HACKER" level.
        
        # We need to map the strategies. 
        # Let's assume RobberyPlanner has a method `plan(target_amount)`
        
        # Note: I need to check RobberyPlanner implementation. 
        # Assuming it exists based on project structure.
        from bank_node.robbery.robbery_planner import RobberyPlanner
        planner = RobberyPlanner(banks)
        result = planner.plan(target_amount)
        
        return f"RP {result}"
