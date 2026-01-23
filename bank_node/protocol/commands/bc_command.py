from typing import List, Any
from bank_node.core.bank import Bank
from bank_node.protocol.commands.base_command import BaseCommand

class BCCommand(BaseCommand):
    """
    Implements the BC (Bank Code) command.
    Returns the bank's IP address.
    """

    def validate_args(self) -> None:
        """
        Validates the arguments.
        For BC command, no arguments are expected, but we ignore them if present
        to ensure robustness.
        """
        pass

    def execute_logic(self) -> Any:
        """
        Retrieves the bank's IP address from the configuration.
        Returns the formatted response string: "BC <ip>"
        """
        server_config = self.bank.config_manager.get("server")
        if server_config and "ip" in server_config:
            ip_address = server_config["ip"]
        else:
            # Fallback default if config is missing or malformed
            ip_address = "127.0.0.1"
            
        return f"BC {ip_address}"
