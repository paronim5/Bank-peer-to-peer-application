from typing import Any
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.protocol.validator import Validator
from bank_node.utils.ip_helper import is_local_ip
from bank_node.network.proxy_client import ProxyClient

class ARCommand(BaseCommand):
    """
    Implements the AR (Account Remove) command.
    """

    def validate_args(self) -> None:
        """
        Validates the arguments for AR command.
        Expects 1 arg: `account_id` (format `num/ip`).
        """
        if len(self.args) != 1:
            raise ValueError("Invalid arguments count. Usage: AR <account_id>")
        
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
        Removes the specified account.
        If the IP is local, removes locally.
        If the IP is remote, forwards the command.
        Returns: "AR"
        """
        account_id = self.args[0]
        account_num = int(account_id.split("/")[0])
        ip_address = account_id.split("/")[1]
        
        if is_local_ip(ip_address):
            try:
                # We use the bank's remove_account method which handles balance check safely
                self.bank.remove_account(account_num)
                return "AR"
            except ValueError as e:
                # Re-raise to be handled by BaseCommand
                raise ValueError(str(e))
        else:
            # Forward to remote bank
            try:
                client = ProxyClient()
                # We send the same command "AR <account_id>" to the remote
                # The remote will parse it, see the IP is local to itself, and execute.
                # Assuming default port 65525 as we don't have port info in AR command
                # Ideally we should look up port from known peers, but standard is 65525
                response = client.send_command(ip_address, 65525, f"AR {account_id}")
                
                if response.startswith("ER"):
                    raise ValueError(response[3:]) # Strip "ER "
                return response
            except Exception as e:
                 raise ValueError(f"Remote execution failed: {str(e)}")
