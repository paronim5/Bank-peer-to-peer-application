from typing import List, Optional, Type, Dict
from bank_node.core.bank import Bank
from bank_node.protocol.commands.base_command import BaseCommand
from bank_node.protocol.command_enum import CommandType

class CommandFactory:
    """
    Factory class to instantiate the correct Command object based on the input string.
    """

    def __init__(self, bank: Bank):
        self.bank = bank
        # Mapping from command code string to Command class type
        self._command_map: Dict[str, Type[BaseCommand]] = {}

    def register_command(self, command_code: str, command_class: Type[BaseCommand]) -> None:
        """
        Registers a command class for a specific command code.
        """
        self._command_map[command_code] = command_class

    def get_command(self, command_code: str, args: List[str]) -> Optional[BaseCommand]:
        """
        Returns an instance of the specific command class based on the command_code.
        Returns None if the command is unknown or invalid.
        """
        if not CommandType.is_valid(command_code):
            return None

        command_class = self._command_map.get(command_code)
        if command_class:
            return command_class(self.bank, args)
        
        return None
