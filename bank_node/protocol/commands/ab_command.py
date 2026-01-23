from typing import Any
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.protocol.validator import Validator
from bank_node.utils.ip_helper import is_local_ip
from bank_node.network.proxy_client import ProxyClient

class ABCommand(BaseCommand):
    """
    Implements the AB (Account Balance) command.
    """

    def validate_args(self) -> None:
        """
        Validates the arguments for AB command.
        Expects 1 arg: `account_id` (format `num/ip`).
        """
        if len(self.args) != 1:
            raise ValueError("Invalid arguments count. Usage: AB <account_id>")
        
        account_id = self.args[0]
        
        # Parse account_id
        if "/" not in account_id:
            raise ValueError("Invalid account_id format. Expected: <number>/<ip>")
        
        parts = account_id.split("/")
        if len(parts) != 2:
            raise ValueError("Invalid account_id format. Expected: <number>/<ip>")
            
        account_num_str, ip_address = parts
        
        # Validate Account Number
        if not account_num_str.isdigit():
             raise ValueError("Account number must be an integer")
        
        account_num = int(account_num_str)
        if not Validator.validate_account_number(account_num):
             raise ValueError("Invalid account number")
             
        # Validate IP
        if not Validator.validate_ip(ip_address):
            raise ValueError("Invalid IP address")

    def execute_logic(self) -> Any:
        """
        Retrieves the balance of the specified account.
        Returns: "AB <balance>"
        """
        account_id = self.args[0]
        parts = account_id.split("/")
        account_num = int(parts[0])
        target_ip = parts[1]
        
        if not is_local_ip(target_ip):
            # Proxy logic
            port = self.bank.config_manager.get("server", {}).get("port", 65525)
            command_string = f"AB {account_id}"
            proxy = ProxyClient()
            return proxy.send_command(target_ip, port, command_string)
        
        balance = self.bank.get_balance(account_num)
        
        return f"AB {balance}"
