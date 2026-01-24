import socket
from bank_node.core.config_manager import ConfigManager

class ProxyClient:
    """
    Client for communicating with other bank nodes.
    Capable of opening a connection, sending a command, and retrieving the response.
    """
    def __init__(self):
        self.config = ConfigManager()
        self.timeout = self.config.get("network", {}).get("proxy_timeout", 5.0)

    def send_command(self, target_ip: str, port: int, command_string: str) -> str:
        """
        Connects to a target bank node, sends a command, and returns the response.

        Args:
            target_ip (str): The IP address of the target bank.
            port (int): The port number of the target bank.
            command_string (str): The command to send (e.g., "BC").

        Returns:
            str: The response from the target bank, or an error message starting with "ER".
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((target_ip, port))
                
                # Send command (ensure newline if not present)
                if not command_string.endswith('\n'):
                    command_string += '\n'
                s.sendall(command_string.encode('utf-8'))
                
                # Receive response
                # A simple recv might be enough for short responses, but robust buffering is better.
                # For this step, "Receive response" usually implies reading until end or some buffer.
                # Let's read a chunk. 4096 is standard.
                response = s.recv(4096)
                return response.decode('utf-8').strip()
                
        except socket.timeout:
            return "ER Timeout"
        except ConnectionRefusedError:
            return "ER Connection failed"
        except Exception as e:
            # Fallback for other errors
            return f"ER {str(e)}"
