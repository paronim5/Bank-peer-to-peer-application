import socket
import threading
import logging
from typing import List
from bank_node.network.client_handler import ClientHandler

class TcpServer:
    """
    The main TCP Server that listens for incoming connections and delegates
    handling to ClientHandler threads.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = False
        self.handlers: List[ClientHandler] = []
        self._lock = threading.Lock()

    def start(self):
        """
        Starts the TCP server to listen for connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reuse of address to avoid "Address already in use" errors on restart
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1.0) # Set timeout to allow periodic checking of is_running
            self.is_running = True
            
            # Resolve actual IP if binding to 0.0.0.0
            display_host = self.host
            if self.host == "0.0.0.0":
                try:
                     from bank_node.utils.ip_helper import get_primary_local_ip
                     display_host = get_primary_local_ip()
                except ImportError:
                    pass

            print(f"TCP Server listening on {self.host}:{self.port} (Actual: {display_host}:{self.port})")

            while self.is_running:
                try:
                    client_socket, address = self.server_socket.accept()
                    self._handle_client(client_socket, address)
                except socket.timeout:
                    # Timeout reached, loop back to check is_running
                    continue
                except OSError:
                    # Socket closed or error
                    if self.is_running:
                        print("Server socket error.")
                    break
        except Exception as e:
            print(f"Failed to start server: {e}")
        finally:
            self.stop()

    def _handle_client(self, client_socket: socket.socket, address):
        """
        Creates and starts a ClientHandler for the connected client.
        """
        handler = ClientHandler(client_socket, address)
        with self._lock:
            self.handlers.append(handler)
        
        # Start the thread
        handler.start()
        
        # Clean up finished handlers periodically (simple approach)
        self._cleanup_handlers()

    def _cleanup_handlers(self):
        """Removes dead threads from the handlers list."""
        with self._lock:
            self.handlers = [h for h in self.handlers if h.is_alive()]

    def stop(self):
        """
        Stops the server and all client handlers.
        """
        self.is_running = False
        
        # Close server socket to unblock accept()
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception as e:
                print(f"Error closing server socket: {e}")
            self.server_socket = None

        # Stop all client handlers
        with self._lock:
            for handler in self.handlers:
                if handler.is_alive():
                    handler.running = False
                    # Closing the socket will force the handler loop to exit if it's blocked on recv
                    try:
                        handler.client_socket.close()
                    except Exception:
                        pass
                    handler.join(timeout=1.0)
            self.handlers.clear()
        
        print("TCP Server stopped.")
