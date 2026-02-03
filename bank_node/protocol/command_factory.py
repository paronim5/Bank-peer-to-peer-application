from typing import List, Optional, Type, Dict
from bank_node.core.bank import Bank
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.protocol.command_enum import CommandType

class CommandFactory:
    """
    Factory class to instantiate the correct Command object based on the input string.
    """

    def __init__(self, bank: Bank):
        """
        Initialize the CommandFactory with a Bank instance.

        Args:
            bank (Bank): The Bank instance to be passed to created commands.
        """
        self.bank = bank
        # Mapping from command code string to Command class type
        self._command_map: Dict[str, Type[BaseCommand]] = {}

    def register_command(self, command_code: str, command_class: Type[BaseCommand]) -> None:
        """
        Register a command class for a specific command code.

        Args:
            command_code (str): The 2-letter command code (e.g., 'BC').
            command_class (Type[BaseCommand]): The class implementing the command.

        Side Effects:
            Updates the internal `_command_map`.
        """
        self._command_map[command_code] = command_class

    def get_command(self, command_code: str, args: List[str]) -> Optional[BaseCommand]:
        """
        Create and return an instance of the specific command class.

        Args:
            command_code (str): The command code to look up.
            args (List[str]): The arguments to pass to the command constructor.

        Returns:
            Optional[BaseCommand]: An instance of the command, or None if the code is invalid/unknown.
        """
        if not CommandType.is_valid(command_code):
            return None

        command_class = self._command_map.get(command_code)
        if command_class:
            return command_class(self.bank, args)
        
        return None
