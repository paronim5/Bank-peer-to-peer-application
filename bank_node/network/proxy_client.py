import socket
import logging

from bank_node.core.config_manager import ConfigManager

class ProxyClient:
    """
    Handles outgoing connections to other bank nodes.
    """
    
    def __init__(self, timeout: int = None):
        if timeout is not None:
            self.timeout = timeout
        else:
            # Load from config or default to 15 seconds (increased from 5 for slower networks)
            config = ConfigManager()
            self.timeout = config.get("network", {}).get("timeout", 15)
            
        self.logger = logging.getLogger("ProxyClient")

    def send_command(self, target_ip: str, port: int, command_string: str) -> str:
        """
        Sends a command to the specified bank and returns the response.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((target_ip, port))
                
                # Ensure command ends with newline
                if not command_string.endswith('\n'):
                    command_string += '\n'
                
                s.sendall(command_string.encode('utf-8'))
                
                # Receive response
                response = s.recv(4096).decode('utf-8').strip()
                return response
                
        except socket.timeout:
            return "ER Timeout"
        except ConnectionRefusedError:
            return "ER Connection refused"
        except Exception as e:
            self.logger.error(f"Error connecting to {target_ip}:{port}: {e}")
            return f"ER {str(e)}"
