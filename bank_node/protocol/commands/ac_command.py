from typing import List, Any
from bank_node.core.bank import Bank
from bank_node.protocol.commands.base_command import BaseCommand

class ACCommand(BaseCommand):
    """
    Implements the AC (Account Create) command.
    Creates a new account and returns the account number and server IP.
    """

    def validate_args(self) -> None:
        """
        Validates the arguments.
        For AC command, no arguments are expected, but we ignore them if present
        to ensure robustness.
        """
        pass

    def execute_logic(self) -> Any:
        """
        Creates a new account via the Bank instance.
        Retrieves the server IP.
        Returns the formatted response string: "AC <number>/<ip>"
        """
        # Create account
        account_number = self.bank.create_account()
        
        # Get server IP
        server_config = self.bank.config_manager.get("server")
        if server_config and "ip" in server_config:
            ip_address = server_config["ip"]
        else:
            ip_address = "127.0.0.1"
            
        return f"AC {account_number}/{ip_address}"
