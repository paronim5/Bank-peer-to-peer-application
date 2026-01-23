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
        Validates if the provided string is a valid IPv4 address.
        """
        if not isinstance(ip_str, str):
            return False
        return bool(Validator._IP_PATTERN.match(ip_str))

    @staticmethod
    def validate_account_number(num: int) -> bool:
        """
        Validates if the account number is an integer between 10000 and 99999.
        """
        if not isinstance(num, int):
            return False
        return 10000 <= num <= 99999

    @staticmethod
    def validate_amount(amount: int) -> bool:
        """
        Validates if the amount is a non-negative integer.
        """
        if not isinstance(amount, int):
            return False
        return amount >= 0

    @staticmethod
    def validate_port(port: int) -> bool:
        """
        Validates if the port is an integer between 65525 and 65535.
        """
        if not isinstance(port, int):
            return False
        return 65525 <= port <= 65535
