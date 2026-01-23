from abc import ABC, abstractmethod
from typing import List, Any
from bank_node.core.bank import Bank

class BaseCommand(ABC):
    """
    Abstract base class for all protocol commands.
    Implements the Template Method pattern for command execution.
    """

    def __init__(self, bank: Bank, args: List[str]):
        """
        Initialize the command with the bank instance and raw arguments.
        
        Args:
            bank: The singleton Bank instance.
            args: List of string arguments passed with the command.
        """
        self.bank = bank
        self.args = args

    @abstractmethod
    def validate_args(self) -> None:
        """
        Validates the arguments passed to the command.
        Raises ValueError if arguments are invalid.
        """
        pass

    @abstractmethod
    def execute_logic(self) -> Any:
        """
        Performs the core business logic of the command.
        Returns the result data to be formatted in the response.
        """
        pass

    def execute(self) -> str:
        """
        Template method that defines the lifecycle of a command execution:
        Validate -> Execute Logic -> Format Response (Success/Error).
        """
        try:
            self.validate_args()
            result = self.execute_logic()
            return self.format_success(result)
        except ValueError as e:
            return self.format_error(str(e))
        except Exception as e:
            # In a real app, log the exception here
            return self.format_error("Internal error")

    def format_success(self, data: Any = None) -> str:
        """
        Formats a success response.
        If data is provided, appends it to the success code (e.g., "AR data").
        Note: The actual command code (e.g. AR) is usually handled by the specific command or parser,
        but for this base, we might assume the subclass knows its code or we return a standard success.
        
        However, based on standard peer-to-peer protocols, the response usually echoes the command code
        or a specific success code.
        
        Let's assume the concrete class will return the full response string or data.
        If `result` is a string, return it.
        """
        # Simplification: The concrete execute_logic returns the string payload or we just return it.
        # But wait, the prompt says: "Helper methods for formatting responses (CODE data vs CODE)".
        # Since we don't have the command code here easily without reflection or passing it,
        # we will assume execute_logic returns the data part, and we might need the command code.
        
        # For now, let's just return the data as string if present, or "OK" if None?
        # Actually, looking at typical implementations, usually the response is constructed by the command.
        # Let's assume execute_logic returns the formatted success message or just the data.
        
        # Refinement based on prompt: "Helper methods for formatting responses"
        # Let's provide generic helpers.
        if data is None:
            return "OK" # Placeholder default
        return str(data)

    def format_error(self, message: str) -> str:
        """
        Formats an error response.
        """
        return f"ERR {message}"
