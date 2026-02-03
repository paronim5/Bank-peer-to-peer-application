from typing import List, Any
from bank_node.core.bank import Bank
from bank_node.protocol.commands.base_command import BaseCommand

class ACCommand(BaseCommand):
    """
    Implements the AC (Account Create) command.

    Creates a new account in the bank and returns the new account number
    combined with the server's IP address.
    """

    def validate_args(self) -> None:
        """
        Validate the arguments.

        For the AC command, no arguments are expected.
        Existing arguments are ignored for robustness.
        """
        pass

    def execute_logic(self) -> Any:
        """
        Execute the AC command logic.

        1. Creates a new account via the Bank instance.
        2. Retrieves the server IP address.
        3. Formats the response as "AC <account_number>/<ip_address>".

        Returns:
            str: The formatted response string.

        Side Effects:
            - Modifies Bank state by creating a new account.
            - Reads from configuration.
        """
        # Create account
        account_number = self.bank.create_account()
        
        # Get server IP
        server_config = self.bank.config_manager.get("server")
        if server_config and "ip" in server_config:
            ip_address = server_config["ip"]
            if ip_address == "0.0.0.0":
                from bank_node.utils.ip_helper import get_primary_local_ip
                ip_address = get_primary_local_ip()
        else:
            ip_address = "127.0.0.1"
            
        return f"AC {account_number}/{ip_address}"
