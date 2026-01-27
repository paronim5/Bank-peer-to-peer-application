import logging
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.protocol.validator import Validator
from bank_node.utils.ip_helper import is_local_ip
from bank_node.network.proxy_client import ProxyClient
from bank_node.core.config_manager import ConfigManager

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
             
        # Validate IP (handle port if present)
        ip_to_validate = ip_address.split(":")[0] if ":" in ip_address else ip_address
        if not Validator.validate_ip(ip_to_validate):
            raise ValueError("Invalid IP address")

    def execute_logic(self) -> str:
        parts = self.args[0].split("/")
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
        
        logging.info(f"ABCommand: target={target_ip} provided_port={provided_port} is_local={is_local}")

        if not is_local:
            clean_account_id = f"{account_num}/{target_ip}"
            command_string = f"AB {clean_account_id}"
            config = ConfigManager()
            proxy_timeout = config.get("network", {}).get("proxy_timeout", 5.0)
            proxy = ProxyClient(timeout=proxy_timeout)
            return proxy.send_command(target_ip, port, command_string)
        
        balance = self.bank.get_balance(account_num)
        
        return f"AB {balance}"
