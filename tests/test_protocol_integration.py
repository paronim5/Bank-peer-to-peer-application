import unittest
from typing import Dict, Any

from bank_node.core.bank import Bank
from bank_node.core.account_repository import AccountRepository
from bank_node.persistence.i_data_store import IDataStore
from bank_node.protocol.command_factory import CommandFactory
from bank_node.protocol.command_parser import CommandParser
from bank_node.protocol.command_enum import CommandType

# Import all commands
from bank_node.protocol.commands.bc_command import BCCommand
from bank_node.protocol.commands.ac_command import ACCommand
from bank_node.protocol.commands.ad_command import ADCommand
from bank_node.protocol.commands.aw_command import AWCommand
from bank_node.protocol.commands.ab_command import ABCommand
from bank_node.protocol.commands.ar_command import ARCommand
from bank_node.protocol.commands.ba_command import BACommand
from bank_node.protocol.commands.bn_command import BNCommand

class InMemoryDataStore(IDataStore):
    def __init__(self):
        self.data = {}
    
    def save_data(self, data: Dict[str, Any]) -> None:
        self.data = data.copy()
    
    def load_data(self) -> Dict[str, Any]:
        return self.data.copy()

class TestProtocolIntegration(unittest.TestCase):
    
    def setUp(self):
        # Reset Bank Singleton
        Bank._instance = None
        
        # Setup Core Components
        self.data_store = InMemoryDataStore()
        self.repository = AccountRepository(self.data_store)
        self.bank = Bank(self.repository)
        
        # Setup Protocol Components
        self.factory = CommandFactory(self.bank)
        self._register_commands()
        
    def _register_commands(self):
        self.factory.register_command(CommandType.BC.value, BCCommand)
        self.factory.register_command(CommandType.AC.value, ACCommand)
        self.factory.register_command(CommandType.AD.value, ADCommand)
        self.factory.register_command(CommandType.AW.value, AWCommand)
        self.factory.register_command(CommandType.AB.value, ABCommand)
        self.factory.register_command(CommandType.AR.value, ARCommand)
        self.factory.register_command(CommandType.BA.value, BACommand)
        self.factory.register_command(CommandType.BN.value, BNCommand)

    def process_command(self, raw_command: str) -> str:
        command_code, args = CommandParser.parse(raw_command)
        if not command_code:
            return "Invalid command"
            
        command = self.factory.get_command(command_code, args)
        if not command:
            return "Unknown command"
            
        return command.execute()

    def test_full_banking_flow(self):
        """
        Simulates a full user session interacting with the bank via protocol commands.
        """
        # 1. Check Bank Code
        response = self.process_command("BC")
        self.assertTrue(response.startswith("BC"), f"Unexpected response: {response}")
        # Note: BC returns local IP, which might vary, but should contain "BC"
        
        # 2. Create Account
        # AC
        response = self.process_command("AC")
        self.assertTrue(response.startswith("AC"), f"Unexpected response: {response}")
        
        # Parse Account ID
        # Format: AC <account_id>/<ip>
        parts = response.split(" ")
        self.assertEqual(len(parts), 2)
        account_info = parts[1]
        account_id_str = account_info.split("/")[0]
        account_id = int(account_id_str)
        
        # 3. Deposit Initial Funds (since AC creates with 0 balance)
        response = self.process_command(f"AD {account_id}/127.0.0.1 1000")
        self.assertEqual(response, "AD")
        
        # 4. Check Balance (Should be 1000)
        response = self.process_command(f"AB {account_id}/127.0.0.1")
        self.assertEqual(response, "AB 1000")
        
        # 5. Deposit More Money
        response = self.process_command(f"AD {account_id}/127.0.0.1 500")
        self.assertEqual(response, "AD")
        
        # 6. Check Balance (Should be 1500)
        response = self.process_command(f"AB {account_id}/127.0.0.1")
        self.assertEqual(response, "AB 1500")
        
        # 7. Withdraw Money
        response = self.process_command(f"AW {account_id}/127.0.0.1 200")
        self.assertEqual(response, "AW")
        
        # 8. Check Balance (Should be 1300)
        response = self.process_command(f"AB {account_id}/127.0.0.1")
        self.assertEqual(response, "AB 1300")
        
        # 9. Bank Amount (Total amount in bank)
        response = self.process_command("BA")
        self.assertEqual(response, "BA 1300")
        
        # 10. Bank Number (Number of clients/accounts)
        response = self.process_command("BN")
        self.assertEqual(response, "BN 1")
        
        # 11. Empty the Account before removal (Requirement for AR)
        response = self.process_command(f"AW {account_id}/127.0.0.1 1300")
        self.assertEqual(response, "AW")
        
        # 12. Remove Account
        response = self.process_command(f"AR {account_id}/127.0.0.1")
        self.assertEqual(response, "AR")
        
        # 13. Verify Account Removed
        response = self.process_command(f"AB {account_id}/127.0.0.1")
        self.assertTrue(response.startswith("ERR"), "Should return error for missing account")
        
        # 14. Verify BN is 0
        response = self.process_command("BN")
        self.assertEqual(response, "BN 0")

    def test_invalid_commands(self):
        response = self.process_command("INVALID")
        self.assertEqual(response, "Invalid command")
        
        response = self.process_command("")
        self.assertEqual(response, "Invalid command")
        
        # Valid format but unknown code (if parser allows it, but parser checks enum)
        # CommandParser.parse returns None if not in Enum usually?
        # Let's check CommandParser behavior. 
        # If I send "XY 123", parser might return ("XY", ["123"]) or None.
        # If parser is strict, it returns None.
        
    def test_persistence_integration(self):
        """
        Verifies that data is actually being saved to the store (Observer pattern check via Bank).
        """
        # Note: AutoSaver is not attached in this test setup unless we do it manually.
        # The integration test in 28-unit-testing.md doesn't explicitly ask for AutoSaver,
        # but it says "Simulate a full flow". 
        # Let's add AutoSaver to verify the full stack integration.
        
        from bank_node.persistence.auto_saver import AutoSaver
        
        auto_saver = AutoSaver(self.repository)
        self.bank.subscribe(auto_saver)
        
        # Create Account
        response = self.process_command("AC")
        
        # Parse Account ID
        parts = response.split(" ")
        account_id_str = parts[1].split("/")[0]
        account_id = int(account_id_str)
        
        # Deposit Funds
        self.process_command(f"AD {account_id}/127.0.0.1 500")
        
        # Check if data store has data
        data = self.data_store.load_data()
        self.assertEqual(len(data), 1, "Data store should have 1 account saved")
        
        # Get the account ID from the saved data
        # Note: keys in json might be strings
        account_id_key = str(account_id)
        self.assertIn(account_id_key, data, "Account ID should be in data store")
        self.assertEqual(data[account_id_key]['balance'], 500)

if __name__ == "__main__":
    unittest.main()
