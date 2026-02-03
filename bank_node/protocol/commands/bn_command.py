from typing import Any
from bank_node.protocol.commands.base_command import BaseCommand

class BNCommand(BaseCommand):
    """
    Implements the BN (Bank Number) command.

    Retrieves and returns the total number of clients (accounts) in the bank.
    """

    def validate_args(self) -> None:
        """
        Validate the arguments for the BN command.

        Expects 0 arguments.

        Raises:
            ValueError: If any arguments are provided.
        """
        if self.args:
            raise ValueError("Invalid arguments count. Usage: BN")

    def execute_logic(self) -> Any:
        """
        Execute the BN command logic.

        Retrieves the client count from the Bank instance.

        Returns:
            str: The formatted response "BN <count>".

        Side Effects:
            Reads account data from the repository.
        """
        count = self.bank.get_client_count()
        return f"BN {count}"
