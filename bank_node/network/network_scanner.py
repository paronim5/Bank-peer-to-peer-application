import ipaddress
import concurrent.futures
from typing import List, Optional
from robbery.bank_info import BankInfo
from bank_node.network.proxy_client import ProxyClient
from bank_node.core.config_manager import ConfigManager

class NetworkScanner:
    """
    Scans the network for active bank nodes and retrieves their information.
    """
    def __init__(self, port: int = 65525, max_workers: int = None):
        self.port = port
        if max_workers is None:
             config = ConfigManager()
             self.max_workers = config.get("network", {}).get("scan_workers", 50)
        else:
            self.max_workers = max_workers
        self.proxy_client = ProxyClient()

    def scan(self, ip_range_start: str, ip_range_end: str) -> List[BankInfo]:
        """
        Scans a range of IPs for bank nodes.
        
        Args:
            ip_range_start (str): Start IP address (e.g., "192.168.1.1").
            ip_range_end (str): End IP address (e.g., "192.168.1.254").
            
        Returns:
            List[BankInfo]: A list of discovered BankInfo objects.
        """
        discovered_banks = []
        
        try:
            # Convert IPs to integers for iteration
            start_ip = int(ipaddress.IPv4Address(ip_range_start))
            end_ip = int(ipaddress.IPv4Address(ip_range_end))
        except ipaddress.AddressValueError:
            return []
        
        ips_to_scan = []
        for ip_int in range(start_ip, end_ip + 1):
            ips_to_scan.append(str(ipaddress.IPv4Address(ip_int)))
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_ip = {executor.submit(self._probe_node, ip): ip for ip in ips_to_scan}
            
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    result = future.result()
                    if result:
                        discovered_banks.append(result)
                except Exception:
                    # Log error if needed, but for scanner we usually ignore failures
                    pass
                    
        return discovered_banks

    def _probe_node(self, ip: str) -> Optional[BankInfo]:
        """
        Probes a single IP to check if it's a bank node and retrieves its info.
        
        Returns:
            BankInfo object if valid bank node found, None otherwise.
        """
        # 1. Send BC (Bank Code) to check connectivity and verify it's a bank
        # BC response format: "BC <ip>"
        response_bc = self.proxy_client.send_command(ip, self.port, "BC")
        if not response_bc.startswith("BC"):
            return None
            
        # 2. Send BA (Bank Amount)
        # BA response format: "BA <amount>"
        response_ba = self.proxy_client.send_command(ip, self.port, "BA")
        total_amount = 0
        if response_ba.startswith("BA"):
            try:
                # Handle potentially missing parts
                parts = response_ba.split()
                if len(parts) > 1:
                    total_amount = int(parts[1])
            except (IndexError, ValueError):
                pass
        
        # 3. Send BN (Bank Number of clients)
        # BN response format: "BN <number>"
        response_bn = self.proxy_client.send_command(ip, self.port, "BN")
        num_clients = 0
        if response_bn.startswith("BN"):
            try:
                parts = response_bn.split()
                if len(parts) > 1:
                    num_clients = int(parts[1])
            except (IndexError, ValueError):
                pass
                
        return BankInfo(ip, total_amount, num_clients)
