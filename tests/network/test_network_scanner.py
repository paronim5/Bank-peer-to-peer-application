import unittest
from unittest.mock import MagicMock
from bank_node.network.network_scanner import NetworkScanner
from robbery.bank_info import BankInfo

class TestNetworkScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = NetworkScanner()
        # Mock the proxy client
        self.scanner.proxy = MagicMock()

    def test_probe_node_success(self):
        # Setup mock responses
        def side_effect(ip, port, cmd):
            if cmd == "BC":
                return f"BC {ip}"
            elif cmd == "BA":
                return "BA 10000"
            elif cmd == "BN":
                return "BN 50"
            return "ER"
            
        self.scanner.proxy.send_command.side_effect = side_effect
        
        result = self.scanner._check_bank("192.168.1.5")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.ip, "192.168.1.5")
        self.assertEqual(result.total_amount, 10000)
        self.assertEqual(result.num_clients, 50)

    def test_probe_node_not_a_bank(self):
        # BC fails
        self.scanner.proxy.send_command.return_value = "ER Connection failed"
        
        result = self.scanner._check_bank("192.168.1.5")
        self.assertIsNone(result)

    def test_probe_node_partial_failure(self):
        # BC works, but BA/BN fail or return garbage
        def side_effect(ip, port, cmd):
            if cmd == "BC":
                return f"BC {ip}"
            elif cmd == "BA":
                return "ER"
            elif cmd == "BN":
                return "BN garbage"
            return "ER"
            
        self.scanner.proxy.send_command.side_effect = side_effect
        
        result = self.scanner._check_bank("192.168.1.5")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.ip, "192.168.1.5")
        self.assertEqual(result.total_amount, 0)
        self.assertEqual(result.num_clients, 0)

    def test_scan_targets(self):
        # Mock proxy_client side_effect for multiple IPs
        def side_effect(ip, port, cmd):
            if ip == "192.168.1.1":
                if cmd == "BC": return "BC 192.168.1.1"
                if cmd == "BA": return "BA 5000"
                if cmd == "BN": return "BN 10"
            elif ip == "192.168.1.2":
                return "ER Connection Refused"
            elif ip == "192.168.1.3":
                if cmd == "BC": return "BC 192.168.1.3"
                if cmd == "BA": return "BA 2000"
                if cmd == "BN": return "BN 5"
            return "ER"

        self.scanner.proxy.send_command.side_effect = side_effect
        
        # Test with explicit targets list
        results = self.scanner.scan(targets=["192.168.1.1", "192.168.1.2", "192.168.1.3"])
        
        # Should find 2 banks (1.1 and 1.3)
        self.assertEqual(len(results), 2)
        
        # Sort by IP to ensure deterministic assertions
        results.sort(key=lambda x: x.ip)
        
        self.assertEqual(results[0].ip, "192.168.1.1")
        self.assertEqual(results[0].total_amount, 5000)
        
        self.assertEqual(results[1].ip, "192.168.1.3")
        self.assertEqual(results[1].total_amount, 2000)

if __name__ == '__main__':
    unittest.main()
