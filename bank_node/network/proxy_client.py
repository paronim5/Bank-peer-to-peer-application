import socket
import logging

class ProxyClient:
    """
    Handles outgoing connections to other bank nodes.
    """
    
    def __init__(self, timeout: float = None):
        if timeout is not None:
            self.timeout = float(timeout)
        else:
            self.timeout = 5.0
            
        self.logger = logging.getLogger("ProxyClient")

    def send_command(self, target_ip: str, port: int, command_string: str) -> str:
        """
        Sends a command to the specified bank and returns the response.
        """
        self.logger.info(f"Attempting to connect to {target_ip}:{port} (Timeout: {self.timeout}s)...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((target_ip, port))
                self.logger.info(f"Connected to {target_ip}:{port}. Sending: {command_string.strip()}")
                
                # Ensure command ends with newline
                if not command_string.endswith('\n'):
                    command_string += '\n'
                
                s.sendall(command_string.encode('utf-8'))
                
                # Receive response
                response = s.recv(4096).decode('utf-8').strip()
                self.logger.info(f"Received response from {target_ip}: {response}")
                return response
                
        except socket.timeout:
            msg = f"Timeout connecting to {target_ip}:{port} after {self.timeout}s"
            self.logger.error(msg)
            return f"ER {msg}"
        except ConnectionRefusedError:
            msg = f"Connection refused by {target_ip}:{port} (Is the bank running there?)"
            self.logger.error(msg)
            return f"ER {msg}"
        except OSError as e:
            if e.winerror == 10065: # WSAEHOSTUNREACH
                msg = f"Host unreachable: {target_ip} (Check VPN/Network connection)"
            elif e.winerror == 10060: # WSAETIMEDOUT
                 msg = f"Connection timed out: {target_ip}"
            else:
                 msg = f"Network error connecting to {target_ip}: {e}"
            self.logger.error(msg)
            return f"ER {msg}"
        except Exception as e:
            self.logger.error(f"Unexpected error connecting to {target_ip}:{port}: {e}")
            return f"ER {str(e)}"
