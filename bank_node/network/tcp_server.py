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
        """
        Initialize the TCP server with a host and port.

        Args:
            host (str): The hostname or IP address to bind to.
            port (int): The port number to listen on.

        Side Effects:
            Initializes the logger and internal state, but does not start listening.
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = False
        self.client_threads = []
        self.logger = logging.getLogger("TcpServer")

    def start(self):
        """
        Start the TCP server to listen for incoming connections.

        This method creates the socket, binds it, and enters a loop to accept
        incoming client connections. It runs until `stop()` is called or an
        unrecoverable error occurs.

        Raises:
            OSError: If socket binding or listening fails.

        Side Effects:
            - Binds to a network port.
            - Blocks the calling thread while running.
            - Spawns new threads for handling clients.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running = True
        self.logger.info(f"Server started on {self.host}:{self.port}")

        try:
            while self.is_running:
                try:
                    self.server_socket.settimeout(1.0)
                    client_socket, address = self.server_socket.accept()
                    self._handle_client(client_socket, address)
                except socket.timeout:
                    continue
                except OSError:
                    break
                finally:
                    self._cleanup_handlers()
        except Exception as e:
            self.logger.error(f"Server error: {e}")
        finally:
            self.stop()

    def _handle_client(self, client_socket: socket.socket, address):
        """
        Handle a new client connection by spawning a handler thread.

        Args:
            client_socket (socket.socket): The connected client socket object.
            address (tuple): The (ip, port) tuple of the client.

        Side Effects:
            - Creates and starts a new ClientHandler thread.
            - Adds the thread to the `client_threads` list.
        """
        self.logger.info(f"New connection from {address}")
        handler = ClientHandler(client_socket, address)
        handler.start()
        self.client_threads.append(handler)

    def _cleanup_handlers(self):
        """
        Remove terminated client handler threads from the list.

        Side Effects:
            Modifies `self.client_threads` by filtering out dead threads.
        """
        self.client_threads = [t for t in self.client_threads if t.is_alive()]

    def stop(self):
        """
        Stop the TCP server and close all connections.

        This method signals the server loop to stop, closes the server socket,
        and waits for active client handlers to terminate.

        Side Effects:
            - Closes the server socket.
            - Joins client handler threads.
            - Sets `self.is_running` to False.
        """
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        for handler in self.client_threads:
            handler.join(timeout=1.0) # Wait for handlers to finish
        self.logger.info("Server stopped")
