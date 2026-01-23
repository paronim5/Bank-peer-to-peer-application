from typing import Any
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.protocol.validator import Validator
from bank_node.utils.ip_helper import is_local_ip
from bank_node.network.proxy_client import ProxyClient

class AWCommand(BaseCommand):
    """
    Implements the AW (Account Withdraw) command.
    """

    def validate_args(self) -> None:
        """
        Validates the arguments for AW command.
        Expects 2 args: `account_id` (format `num/ip`) and `amount`.
        """
        if len(self.args) != 2:
            raise ValueError("Invalid arguments count. Usage: AW <account_id> <amount>")
        
        account_id = self.args[0]
        amount_str = self.args[1]
        
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
            
        # Foreign IP check removed to support Proxying

        # Validate Amount
        try:
            amount = int(amount_str)
        except ValueError:
            raise ValueError("Amount must be an integer")
            
        if amount <= 0:
            raise ValueError("Amount must be positive")

    def execute_logic(self) -> Any:
        """
        Withdraws money from the specified account.
        """
        account_id = self.args[0]
        amount = int(self.args[1])
        parts = account_id.split("/")
        account_num = int(parts[0])
        target_ip = parts[1]
        
        if not is_local_ip(target_ip):
            # Proxy logic
            port = self.bank.config_manager.get("server", {}).get("port", 65525)
            command_string = f"AW {account_id} {amount}"
            proxy = ProxyClient()
            return proxy.send_command(target_ip, port, command_string)
        
        try:
            self.bank.withdraw(account_num, amount)
            return "AW"
        except ValueError as e:
            # If the bank raises ValueError (e.g. insufficient funds), we catch it
            # and re-raise or return the error format. 
            # The BaseCommand.execute catches ValueError and returns "ERR <msg>".
            # The requirement says: Error format: `ER Insufficient funds.`
            # If I raise ValueError("Insufficient funds."), BaseCommand returns "ERR Insufficient funds."
            # Wait, the requirement says "ER", BaseCommand says "ERR".
            # I should check BaseCommand.format_error.
            raise ValueError(str(e))

    def format_error(self, message: str) -> str:
        return f"ER {message}"
