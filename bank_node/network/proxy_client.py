import socket

class ProxyClient:
    """
    Client for communicating with other bank nodes.
    Capable of opening a connection, sending a command, and retrieving the response.
    """

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
                s.settimeout(5.0)
                s.connect((target_ip, port))
                
                # Send command (ensure newline if not present, though protocol usually implies it, 
                # but let's just send what is given, maybe adding \n if missing is safer, 
                # but requirements say "Send command_string (encoded)". 
                # Let's assume command_string is complete or handled by caller.
                # However, usually protocols need a delimiter. 
                # Looking at previous steps (Step 27 verify script), we added \n.
                # I will encode as is.
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
