class BankInfo:
    """
    DTO to store discovered bank information.
    """
    def __init__(self, ip: str, total_amount: int, num_clients: int):
        self.ip = ip
        self.total_amount = total_amount
        self.num_clients = num_clients

    @property
    def ratio(self) -> float:
        """
        Calculates the ratio of total amount to number of clients.
        Returns 0.0 if num_clients is 0 to avoid division by zero.
        """
        if self.num_clients == 0:
            return 0.0
        return self.total_amount / self.num_clients

    def __repr__(self) -> str:
        return f"BankInfo(ip='{self.ip}', total_amount={self.total_amount}, num_clients={self.num_clients}, ratio={self.ratio:.2f})"
