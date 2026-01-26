class BankInfo:
    """
    Data Transfer Object (DTO) to store information about a discovered bank.
    """
    def __init__(self, ip: str, port: int, total_amount: int, num_clients: int):
        self.ip = ip
        self.port = port
        self.total_amount = total_amount
        self.num_clients = num_clients

    @property
    def ratio(self) -> float:
        """
        Returns the ratio of total_amount / num_clients.
        Higher ratio means more money per client (better target).
        """
        if self.num_clients == 0:
            return 0.0
        return self.total_amount / self.num_clients

    def __repr__(self):
        return f"Bank({self.ip}:{self.port}, ${self.total_amount}, {self.num_clients} clients)"
