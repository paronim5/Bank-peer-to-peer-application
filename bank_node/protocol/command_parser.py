from typing import Tuple, List, Optional
from bank_node.protocol.command_enum import CommandType

class CommandParser:
    """
    Parses raw incoming strings into a command code and a list of arguments.
    """
    
    @staticmethod
    def parse(raw_data: str) -> Tuple[Optional[str], List[str]]:
        """
        Parse a raw input string into a command code and arguments.

        Args:
            raw_data (str): The raw string received from the network.

        Returns:
            Tuple[Optional[str], List[str]]: A tuple containing:
                - The command code (str) if valid, or None if invalid/empty.
                - A list of argument strings (List[str]).

        Example:
            >>> CommandParser.parse("BC 192.168.1.1 8080")
            ('BC', ['192.168.1.1', '8080'])
        """
        if not raw_data:
            return None, []
        
        # Strip whitespace and split by spaces
        parts = raw_data.strip().split()
        
        if not parts:
            return None, []
        
        command_code = parts[0]
        
        # Validate against Enum
        if CommandType.is_valid(command_code):
            return command_code, parts[1:]
        
        # If invalid command code, return None
        return None, []
