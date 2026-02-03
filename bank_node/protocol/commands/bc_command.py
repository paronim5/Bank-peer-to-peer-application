from typing import List, Any
from bank_node.core.bank import Bank
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.utils.ip_helper import get_primary_local_ip

class BCCommand(BaseCommand):
    """
    Implements the BC (Bank Connect/Check) command.

    Retrieves and returns the bank's IP address.
    """

    def validate_args(self) -> None:
        """
        Validate the arguments.

        For the BC command, no arguments are expected.
        Existing arguments are ignored for robustness.
        """
        pass

    def execute_logic(self) -> Any:
        """
        Execute the BC command logic.

        Retrieves the configured server IP address. If the IP is '0.0.0.0',
        it attempts to resolve the primary local IP.

        Returns:
            str: The formatted response "BC <ip_address>".

        Side Effects:
            Reads from the configuration manager.
        """
        server_config = self.bank.config_manager.get("server")
        ip_address = "127.0.0.1"
        if server_config and "ip" in server_config:
            ip_address = server_config["ip"]
            if ip_address == "0.0.0.0":
                ip_address = get_primary_local_ip()
            
        return f"BC {ip_address}"
