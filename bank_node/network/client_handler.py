import threading
import socket
import logging
from typing import Tuple

from bank_node.core.bank import Bank
from bank_node.core.config_manager import ConfigManager
from bank_node.protocol.command_factory import CommandFactory
from bank_node.protocol.command_parser import CommandParser
from bank_node.protocol.command_enum import CommandType

# Import all available commands
from bank_node.protocol.commands.bc_command import BCCommand
from bank_node.protocol.commands.ac_command import ACCommand
from bank_node.protocol.commands.ad_command import ADCommand
from bank_node.protocol.commands.aw_command import AWCommand
from bank_node.protocol.commands.ab_command import ABCommand
from bank_node.protocol.commands.ar_command import ARCommand
from bank_node.protocol.commands.ba_command import BACommand
from bank_node.protocol.commands.bn_command import BNCommand
from bank_node.protocol.commands.rp_command import RPCommand

class ClientHandler(threading.Thread):
    """
    Handles individual client connections in a separate thread.
    """

    def __init__(self, client_socket: socket.socket, address: Tuple[str, int]):
        super().__init__()
        self.client_socket = client_socket
        self.address = address
        self.running = True
        self.buffer = ""
        
        # Initialize Bank and Factory
        self.bank = Bank()
        self.factory = CommandFactory(self.bank)
        self._register_commands()
        
        # Set a timeout for the socket operations (e.g., 60 seconds)
        config = ConfigManager()
        timeout = config.get("network", {}).get("client_timeout", 60.0)
        self.client_socket.settimeout(timeout)

    def _register_commands(self):
        """Registers all supported commands with the factory."""
        self.factory.register_command(CommandType.BC.value, BCCommand)
        self.factory.register_command(CommandType.AC.value, ACCommand)
        self.factory.register_command(CommandType.AD.value, ADCommand)
        self.factory.register_command(CommandType.AW.value, AWCommand)
        self.factory.register_command(CommandType.AB.value, ABCommand)
        self.factory.register_command(CommandType.AR.value, ARCommand)
        self.factory.register_command(CommandType.BA.value, BACommand)
        self.factory.register_command(CommandType.BN.value, BNCommand)
        self.factory.register_command(CommandType.RP.value, RPCommand)

    def run(self):
        """
        Main loop to receive and process data from the client.
        """
        print(f"Connection from {self.address} established.")
        
        try:
            while self.running:
                try:
                    data = self.client_socket.recv(1024)
                    if not data:
                        # Client disconnected
                        break
                    
                    self.buffer += data.decode('utf-8')
                    
                    # Process complete messages delimited by newline
                    while '\n' in self.buffer:
                        message, self.buffer = self.buffer.split('\n', 1)
                        response = self._process_message(message)
                        if response:
                            self.client_socket.sendall((response + '\n').encode('utf-8'))
                            
                except socket.timeout:
                    # Handle timeout - maybe just continue or close?
                    # For now, we'll close the connection on timeout to free resources
                    print(f"Connection from {self.address} timed out.")
                    break
                    
        except ConnectionResetError:
            print(f"Connection from {self.address} reset.")
        except Exception as e:
            print(f"Error handling client {self.address}: {e}")
        finally:
            self.client_socket.close()
            print(f"Connection from {self.address} closed.")

    def _process_message(self, message: str) -> str:
        """
        Parses and executes a single message.
        """
        try:
            if not message.strip():
                return "Invalid command"

            command_code, args = CommandParser.parse(message)
            
            if not command_code:
                return "Invalid command format"
            
            command = self.factory.get_command(command_code, args)
            
            if command:
                return command.execute()
            else:
                return "Unknown command"
                
        except Exception as e:
            return f"Error executing command: {str(e)}"
