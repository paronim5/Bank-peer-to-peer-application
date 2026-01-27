import ipaddress
import concurrent.futures
import logging
from typing import List, Optional
from bank_node.network.proxy_client import ProxyClient
from bank_node.robbery.bank_info import BankInfo
from bank_node.core.config_manager import ConfigManager

class NetworkScanner:
    """
    Scans the network for other active bank nodes.
    """

    def __init__(self, port: int = 65525, workers: int = None, timeout: int = 1):
        self.port = port
        config = ConfigManager()
        network_cfg = config.get("network", {}) or {}
        self.workers = workers if workers is not None else network_cfg.get("scan_workers", 50)
        self.timeout = timeout
        self.logger = logging.getLogger("NetworkScanner")
        self.proxy = ProxyClient(timeout=self.timeout)

    def scan(self, ip_range_start: str, ip_range_end: str) -> List[BankInfo]:
        """
        Scans a range of IPs to find active banks.
        Returns a list of BankInfo objects.
        """
        active_banks: List[BankInfo] = []
        
        try:
            start_ip = ipaddress.IPv4Address(ip_range_start)
            end_ip = ipaddress.IPv4Address(ip_range_end)
            
            # Generate IP list
            ips_to_scan = [str(ipaddress.IPv4Address(ip)) for ip in range(int(start_ip), int(end_ip) + 1)]
            
            self.logger.info(f"Scanning {len(ips_to_scan)} IPs from {ip_range_start} to {ip_range_end}...")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
                # Map IPs to the check_bank method
                future_to_ip = {executor.submit(self._check_bank, ip): ip for ip in ips_to_scan}
                
                for future in concurrent.futures.as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    try:
                        bank_info = future.result()
                        if bank_info:
                            active_banks.append(bank_info)
                    except Exception as e:
                        self.logger.error(f"Error scanning {ip}: {e}")
                        
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")

        return active_banks

    def _check_bank(self, ip: str) -> Optional[BankInfo]:
        """
        Checks if a specific IP is a bank node.
        1. Send BC (Bank Code) -> Expect "BC <ip>"
        2. Send BA (Bank Amount) -> Expect "BA <amount>"
        3. Send BN (Bank Number) -> Expect "BN <count>"
        """
        # 1. Check if it's a bank (BC)
        response_bc = self.proxy.send_command(ip, self.port, "BC")
        if not response_bc.startswith("BC"):
            return None
        
        # 2. Get Total Amount (BA)
        response_ba = self.proxy.send_command(ip, self.port, "BA")
        total_amount = 0
        if response_ba.startswith("BA"):
            try:
                total_amount = int(response_ba.split()[1])
            except (IndexError, ValueError):
                pass
        
        # 3. Get Client Count (BN)
        response_bn = self.proxy.send_command(ip, self.port, "BN")
        client_count = 0
        if response_bn.startswith("BN"):
            try:
                client_count = int(response_bn.split()[1])
            except (IndexError, ValueError):
                pass
                
        self.logger.info(f"Found bank at {ip}: ${total_amount}, {client_count} clients")
        return BankInfo(ip, self.port, total_amount, client_count)
