from typing import Any
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.protocol.validator import Validator
from bank_node.utils.ip_helper import is_local_ip
from bank_node.network.proxy_client import ProxyClient
from bank_node.core.config_manager import ConfigManager

class ADCommand(BaseCommand):
    """
    Implements the AD (Account Deposit) command.

    Handles depositing money into an account. Supports both local deposits
    and forwarding deposit requests to remote bank nodes.
    """

    def validate_args(self) -> None:
        """
        Validate the arguments for the AD command.

        Expects exactly 2 arguments:
        1. `account_id` in the format `<number>/<ip>` (e.g., "12345/192.168.1.1").
        2. `amount` as a positive integer.

        Raises:
            ValueError: If argument count is wrong, formats are invalid, or values are out of range.
        """
        if len(self.args) != 2:
            raise ValueError("Invalid arguments count. Usage: AD <account_id> <amount>")
        
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
             
        # Validate IP (handle port if present)
        ip_to_validate = ip_address.split(":")[0] if ":" in ip_address else ip_address
        if not Validator.validate_ip(ip_to_validate):
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
        Execute the AD command logic.

        If the target account is local, deposits the amount directly.
        If the target account is remote, forwards the command via `ProxyClient`.

        Returns:
            str: "AD" on success, or the response from the remote node.

        Side Effects:
            - Modifies account balance (local).
            - Initiates network connection (remote).
        """
        account_id = self.args[0]
        amount = int(self.args[1])
        parts = account_id.split("/")
        account_num = int(parts[0])
        target_ip_full = parts[1]
        
        target_ip = target_ip_full
        port = self.bank.config_manager.get("server", {}).get("port", 65525)
        provided_port = None

        if ":" in target_ip:
            target_ip, port_str = target_ip.split(":")
            try:
                provided_port = int(port_str)
                port = provided_port
            except ValueError:
                pass

        # Check if local
        is_local = is_local_ip(target_ip)
        if is_local and provided_port is not None:
             local_port = self.bank.config_manager.get("server", {}).get("port", 65525)
             if provided_port != local_port:
                 is_local = False

        if not is_local:
            clean_account_id = f"{account_num}/{target_ip}"
            command_string = f"AD {clean_account_id} {amount}"
            config = ConfigManager()
            proxy_timeout = config.get("network", {}).get("proxy_timeout", 5.0)
            proxy = ProxyClient(timeout=proxy_timeout)
            return proxy.send_command(target_ip, port, command_string)

        self.bank.deposit(account_num, amount)
        
        return "AD"
