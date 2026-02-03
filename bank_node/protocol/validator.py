import re

class Validator:
    """
    Utility class to enforce protocol rules and validate data formats.
    """
    
    # IPv4 Regex pattern
    _IP_PATTERN = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

    @staticmethod
    def validate_ip(ip_str: str) -> bool:
        """
        Validate if the provided string is a valid IPv4 address.

        Args:
            ip_str (str): The IP string to check.

        Returns:
            bool: True if it matches the IPv4 pattern, False otherwise.
        """
        if not isinstance(ip_str, str):
            return False
        return bool(Validator._IP_PATTERN.match(ip_str))

    @staticmethod
    def validate_account_number(num: int) -> bool:
        """
        Validate if the account number is within the valid range (10000-99999).

        Args:
            num (int): The account number.

        Returns:
            bool: True if 10000 <= num <= 99999.
        """
        if not isinstance(num, int):
            return False
        return 10000 <= num <= 99999

    @staticmethod
    def validate_amount(amount: int) -> bool:
        """
        Validate if the amount is non-negative.

        Args:
            amount (int): The monetary amount.

        Returns:
            bool: True if amount >= 0.
        """
        if not isinstance(amount, int):
            return False
        return amount >= 0

    @staticmethod
    def validate_port(port: int) -> bool:
        """
        Validate if the port is within the allowed range (65525-65535).

        Args:
            port (int): The port number.

        Returns:
            bool: True if 65525 <= port <= 65535.
        """
        if not isinstance(port, int):
            return False
        return 65525 <= port <= 65535
