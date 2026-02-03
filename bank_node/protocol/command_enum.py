from enum import Enum

class CommandType(Enum):
    """
    Enum defining the available commands in the peer-to-peer bank protocol.
    """
    BC = "BC" # Bank Connect/Check? (Context dependent, usually predefined)
    AC = "AC" # Account Create?
    AD = "AD" # Account Deposit?
    AW = "AW" # Account Withdraw?
    AB = "AB" # Account Balance?
    AR = "AR" # Account Remove?
    BA = "BA" # Bank Amount? (Total capital)
    BN = "BN" # Bank Number? (Client count)

    @staticmethod
    def is_valid(command: str) -> bool:
        """
        Check if the provided command string is a valid command type.

        Args:
            command (str): The command code to check.

        Returns:
            bool: True if the command is in the Enum values, False otherwise.
        """
        return any(command == item.value for item in CommandType)
