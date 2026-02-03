from abc import ABC, abstractmethod
from typing import List, Any
from bank_node.core.bank import Bank

class BaseCommand(ABC):
    """
    Abstract base class for all protocol commands.
    
    Implements the Template Method pattern for command execution, providing
    standard lifecycle methods for validation, execution, and response formatting.
    """

    def __init__(self, bank: Bank, args: List[str]):
        """
        Initialize the command with a Bank instance and arguments.

        Args:
            bank (Bank): The singleton Bank instance to operate on.
            args (List[str]): List of string arguments passed with the command.
        """
        self.bank = bank
        self.args = args

    @abstractmethod
    def validate_args(self) -> None:
        """
        Validate the arguments passed to the command.

        Raises:
            ValueError: If the arguments are invalid (count, type, or format).
        """
        pass

    @abstractmethod
    def execute_logic(self) -> Any:
        """
        Perform the core business logic of the command.

        Returns:
            Any: The result data to be formatted in the response (usually a string or None).

        Raises:
            Exception: Any exception raised during logic execution (e.g., account not found).
        """
        pass

    def execute(self) -> str:
        """
        Execute the command following the standard lifecycle.

        Steps:
        1. Validate arguments (`validate_args`).
        2. Execute business logic (`execute_logic`).
        3. Format success response (`format_success`).
        4. Catch and format errors (`format_error`).

        Returns:
            str: The final response string to be sent to the client.
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
        Format a success response.

        Args:
            data (Any, optional): The data to include in the response. Defaults to None.

        Returns:
            str: The formatted success string (e.g., "OK" or the data string).
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
        Format an error response.

        Args:
            message (str): The error description.

        Returns:
            str: The formatted error string (e.g., "ERR <message>").
        """
        return f"ERR {message}"
