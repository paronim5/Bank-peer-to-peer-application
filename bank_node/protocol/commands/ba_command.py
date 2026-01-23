from typing import Any
from bank_node.protocol.commands.base_command import BaseCommand

class BACommand(BaseCommand):
    """
    Implements the BA (Bank Amount) command to get the total money in the bank.
    """

    def validate_args(self) -> None:
        """
        Validates the arguments for BA command.
        Expects 0 args.
        """
        if self.args:
            raise ValueError("Invalid arguments count. Usage: BA")

    def execute_logic(self) -> Any:
        """
        Gets the total capital in the bank.
        Returns: "BA <amount>"
        """
        total = self.bank.get_total_capital()
        return f"BA {total}"
