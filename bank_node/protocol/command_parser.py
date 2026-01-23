from typing import Tuple, List, Optional
from bank_node.protocol.command_enum import CommandType

class CommandParser:
    """
    Parses raw incoming strings into a command code and a list of arguments.
    """
    
    @staticmethod
    def parse(raw_data: str) -> Tuple[Optional[str], List[str]]:
        """
        Parses the raw input string.
        
        Args:
            raw_data: The raw string received from the network.
            
        Returns:
            A tuple containing the command code (or None if invalid) and a list of arguments.
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
