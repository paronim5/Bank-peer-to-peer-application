from typing import Any
from bank_node.protocol.commands.base_command import BaseCommand

class BNCommand(BaseCommand):
    """
    Implements the BN (Bank Number) command to get the number of clients.
    """

    def validate_args(self) -> None:
        """
        Validates the arguments for BN command.
        Expects 0 args.
        """
        if self.args:
            raise ValueError("Invalid arguments count. Usage: BN")

    def execute_logic(self) -> Any:
        """
        Gets the number of clients in the bank.
        Returns: "BN <number>"
        """
        count = self.bank.get_client_count()
        return f"BN {count}"
