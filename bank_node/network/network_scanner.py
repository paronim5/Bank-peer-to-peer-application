import ipaddress
import concurrent.futures
import logging
from typing import List, Optional
from bank_node.network.proxy_client import ProxyClient
from bank_node.robbery.bank_info import BankInfo
from bank_node.core.config_manager import ConfigManager
from bank_node.utils.ip_helper import get_primary_local_ip, get_local_subnet_range

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

    def scan(self, targets: List[str] = None) -> List[BankInfo]:
        """
        Scans a list of CIDR ranges or IPs to find active banks.
        Args:
            targets: List of strings, e.g., ["10.0.0.0/24", "192.168.1.50"]
                     If None, loads 'scan_targets' from config.
        Returns:
            List of BankInfo objects.
        """
        active_banks: List[BankInfo] = []
        
        if targets is None:
            config = ConfigManager()
            network_cfg = config.get("network", {})
            # Default to a safe local scan if nothing configured
            targets = network_cfg.get("scan_targets", [])
            
            if not targets:
                 # If config is empty, default to scanning local subnet + localhost
                 local_ip = get_primary_local_ip()
                 # Assuming /24 for local subnet if not specified
                 # We can use the helper to get a CIDR string or just a range
                 # But NetworkScanner supports CIDR string.
                 # Let's construct a CIDR based on local IP.
                 if local_ip and local_ip != "127.0.0.1":
                     # Simple heuristic: assume /24
                     subnet = ".".join(local_ip.split(".")[:3]) + ".0/24"
                     targets = [subnet, "127.0.0.1"]
                 else:
                     targets = ["127.0.0.1"]

        self.logger.info(f"Starting network scan on targets: {targets}")
        
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
                futures = {}
                
                for target in targets:
                    try:
                        # Handle CIDR (e.g., 10.0.0.0/24) or single IP
                        if "/" in target:
                            network = ipaddress.IPv4Network(target, strict=False)
                            self.logger.info(f"Queueing scan for network {target} ({network.num_addresses} hosts)...")
                            for ip in network.hosts():
                                futures[executor.submit(self._check_bank, str(ip))] = str(ip)
                        else:
                            # Single IP
                            futures[executor.submit(self._check_bank, target)] = target
                            
                    except ValueError as e:
                        self.logger.error(f"Invalid target format '{target}': {e}")

                self.logger.info(f"Waiting for {len(futures)} scan tasks to complete...")
                
                for future in concurrent.futures.as_completed(futures):
                    ip = futures[future]
                    try:
                        bank_info = future.result()
                        if bank_info:
                            active_banks.append(bank_info)
                    except Exception as e:
                        # Log at debug to avoid flooding logs with "Connection refused"
                        self.logger.debug(f"Scan result for {ip}: {e}")
                        
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")

        self.logger.info(f"Scan complete. Found {len(active_banks)} active banks.")
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
