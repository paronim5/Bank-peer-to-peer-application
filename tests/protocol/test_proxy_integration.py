import unittest
from unittest.mock import patch, MagicMock
from bank_node.protocol.commands.ad_command import ADCommand
from bank_node.protocol.commands.aw_command import AWCommand
from bank_node.protocol.commands.ab_command import ABCommand
from bank_node.core.bank import Bank

class TestProxyIntegration(unittest.TestCase):
    
    def setUp(self):
        self.bank = MagicMock(spec=Bank)
        self.bank.config_manager = MagicMock()
        self.bank.config_manager.get.return_value = {"ip": "127.0.0.1", "port": 65525}

    @patch('bank_node.protocol.commands.ad_command.ProxyClient')
    @patch('bank_node.protocol.commands.ad_command.is_local_ip')
    def test_ad_proxy_foreign_ip(self, mock_is_local, mock_proxy_cls):
        # Setup
        mock_is_local.return_value = False
        mock_proxy = MagicMock()
        mock_proxy_cls.return_value = mock_proxy
        mock_proxy.send_command.return_value = "AD"
        
        command = ADCommand(self.bank, ["10000/192.168.1.5", "500"])
        result = command.execute()
        
        # Verify
        mock_is_local.assert_called_with("192.168.1.5")
        mock_proxy.send_command.assert_called_with("192.168.1.5", 65525, "AD 10000/192.168.1.5 500")
        self.assertEqual(result, "AD")
        self.bank.deposit.assert_not_called()

    @patch('bank_node.protocol.commands.ad_command.ProxyClient')
    @patch('bank_node.protocol.commands.ad_command.is_local_ip')
    def test_ad_local_ip(self, mock_is_local, mock_proxy_cls):
        # Setup
        mock_is_local.return_value = True
        
        command = ADCommand(self.bank, ["10000/127.0.0.1", "500"])
        result = command.execute()
        
        # Verify
        mock_proxy_cls.assert_not_called()
        self.bank.deposit.assert_called_with(10000, 500)
        self.assertEqual(result, "AD")

    @patch('bank_node.protocol.commands.aw_command.ProxyClient')
    @patch('bank_node.protocol.commands.aw_command.is_local_ip')
    def test_aw_proxy_foreign_ip(self, mock_is_local, mock_proxy_cls):
        # Setup
        mock_is_local.return_value = False
        mock_proxy = MagicMock()
        mock_proxy_cls.return_value = mock_proxy
        mock_proxy.send_command.return_value = "AW"
        
        command = AWCommand(self.bank, ["10000/192.168.1.5", "200"])
        result = command.execute()
        
        # Verify
        mock_proxy.send_command.assert_called_with("192.168.1.5", 65525, "AW 10000/192.168.1.5 200")
        self.assertEqual(result, "AW")
        self.bank.withdraw.assert_not_called()

    @patch('bank_node.protocol.commands.ab_command.ProxyClient')
    @patch('bank_node.protocol.commands.ab_command.is_local_ip')
    def test_ab_proxy_foreign_ip(self, mock_is_local, mock_proxy_cls):
        # Setup
        mock_is_local.return_value = False
        mock_proxy = MagicMock()
        mock_proxy_cls.return_value = mock_proxy
        mock_proxy.send_command.return_value = "AB 10000"
        
        command = ABCommand(self.bank, ["10000/192.168.1.5"])
        result = command.execute()
        
        # Verify
        mock_proxy.send_command.assert_called_with("192.168.1.5", 65525, "AB 10000/192.168.1.5")
        self.assertEqual(result, "AB 10000")
        self.bank.get_balance.assert_not_called()

if __name__ == '__main__':
    unittest.main()
