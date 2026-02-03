import socket
import logging

class ProxyClient:
    """
    Handles outgoing connections to other bank nodes.
    """
    
    def __init__(self, timeout: float = 5.0):
        """
        Initialize the ProxyClient.

        Args:
            timeout (float): Connection timeout in seconds. Defaults to 5.0.
        """
        self.timeout = timeout
        self.logger = logging.getLogger("ProxyClient")

    def send_command(self, target_ip: str, port: int, command_string: str) -> str:
        """
        Send a command to a remote bank node and return the response.

        Args:
            target_ip (str): The IP address of the target node.
            port (int): The port number of the target node.
            command_string (str): The raw command string to send.

        Returns:
            str: The response from the remote node, or an error message starting with 'ER'.

        Raises:
            None: Exceptions are caught and returned as error strings.

        Side Effects:
            - Opens a TCP connection to the target.
            - Sends data over the network.
        """
        try:
            with socket.create_connection((target_ip, port), timeout=self.timeout) as sock:
                sock.sendall(f"{command_string}\n".encode('utf-8'))
                response = sock.recv(4096).decode('utf-8').strip()
                return response
        except socket.timeout:
            self.logger.error(f"Timeout connecting to {target_ip}:{port}")
            return "ER Connection timed out"
        except ConnectionRefusedError:
            self.logger.error(f"Connection refused by {target_ip}:{port}")
            return "ER Connection refused"
        except Exception as e:
            self.logger.error(f"Error sending command to {target_ip}:{port}: {e}")
            return f"ER Network error: {str(e)}"
