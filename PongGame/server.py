import socket
import threading
import pickle

class PongServer:
    """
    PongServer class for managing a Pong game server.

    Attributes:
    - host (str): The host IP address to bind the server.
    - port (int): The port number to bind the server.
    - game_state (dict): Current state of the Pong game.
    - clients (list): List of connected clients (sockets).
    - server_socket (socket): The main server socket.

    Methods:
    - start(): Start the Pong server and listen for incoming connections.
    - handle_client(client_socket, addr): Handle communication with a connected client.
    - update_game_state(client_input): Update the game state based on client input.
    - broadcast_game_state(): Broadcast the current game state to all connected clients.
    """

    # ANSI escape codes for colors
    RESET = '\033[0m'
    GREEN = '\033[92m'
    RED = '\033[91m'

    def __init__(self, host, port):
        """
        Initialize the PongServer instance.

        Parameters:
        - host (str): The host IP address to bind the server.
        - port (int): The port number to bind the server.
        """
        self.host = host
        self.port = port
        self.game_state = {
            'player1': {'y': 250},
            'player2': {'y': 250},
            'ball': {'x': 400, 'y': 300, 'dx': 5, 'dy': 5},
            'score': {'player1': 0, 'player2': 0}
        }
        self.clients = []
        self.server_socket = None

    def start(self):
        """
        Start the Pong server and listen for incoming connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print(f"{self.GREEN}Server listening on {self.host}:{self.port}{self.RESET}")

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_handler.start()

        except KeyboardInterrupt:
            print(f"{self.RED}\nServer shutting down...{self.RESET}")
            self.server_socket.close()
            for client in self.clients:
                client.close()
            print(f"{self.RED}Server and all clients closed.{self.RESET}")

    def handle_client(self, client_socket, addr):
        """
        Handle communication with a connected client.

        Parameters:
        - client_socket (socket): The socket object representing the connected client.
        - addr (tuple): The address (IP, port) of the connected client.
        """
        print(f"{self.GREEN}Connection from {addr} established.{self.RESET}")
        self.clients.append(client_socket)

        while True:
            try:
                data = client_socket.recv(1024)

                if not data:
                    print(f"{self.GREEN}Connection from {addr} closed.{self.RESET}")
                    self.clients.remove(client_socket)
                    break

                client_input = pickle.loads(data)
                self.update_game_state(client_input)
                self.broadcast_game_state()

            except Exception as e:
                print(f"{self.RED}Error handling client {addr}: {e}{self.RESET}")
                self.clients.remove(client_socket)
                break

    def update_game_state(self, client_input):
        """
        Update the game state based on client input.

        Parameters:
        - client_input (dict): Input received from a client.
        """
        if 'player' in client_input and 'y' in client_input:
            self.game_state[client_input['player']]['y'] = client_input['y']

    def broadcast_game_state(self):
        """
        Broadcast the current game state to all connected clients.
        """
        serialized_game_state = pickle.dumps(self.game_state)
        for client in self.clients:
            try:
                client.send(serialized_game_state)
            except Exception as e:
                print(f"{self.RED}Error broadcasting to a client: {e}{self.RESET}")

if __name__ == "__main__":
    server = PongServer(host='127.0.0.1', port=5555)
    server.start()
