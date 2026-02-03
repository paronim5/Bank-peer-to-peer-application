from typing import Any
from bank_node.protocol.commands.base_command import BaseCommand

class BACommand(BaseCommand):
    """
    Implements the BA (Bank Amount) command.

    Calculates and returns the total amount of money held in the bank
    across all accounts.
    """

    def validate_args(self) -> None:
        """
        Validate the arguments for the BA command.

        Expects 0 arguments.

        Raises:
            ValueError: If any arguments are provided.
        """
        if self.args:
            raise ValueError("Invalid arguments count. Usage: BA")

    def execute_logic(self) -> Any:
        """
        Execute the BA command logic.

        Retrieves the total capital from the Bank instance.

        Returns:
            str: The formatted response "BA <total_amount>".

        Side Effects:
            Reads account data from the repository.
        """
        total = self.bank.get_total_capital()
        return f"BA {total}"
