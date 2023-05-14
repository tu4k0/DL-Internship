import socket
import requests

from abc import abstractmethod, ABC


class BaseBlockchain(ABC):
    socket: socket
    node: socket
    ip_address: str
    port: int
    requests: int
    responses: int
    commands: list

    def __init__(self):
        self.requests = 0
        self.responses = 0

    @abstractmethod
    def create_message(self, *data):
        pass

    @abstractmethod
    def create_getdata_payload(self, *data):
        pass

    @abstractmethod
    def create_ping_payload(self):
        pass

    @staticmethod
    def get_ip() -> str:
        ip = requests.get('https://checkip.amazonaws.com').text.strip()

        return ip

    def set_socket(self) -> socket.socket:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if str(self.socket.type) == 'SocketKind.SOCK_STREAM':
            return self.socket
        else:
            raise Exception('Failed to set socket')

    def set_node(self) -> socket.socket:
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_connections(self, node_num) -> str:
        if self.node is None:
            raise Exception('Node not set yet')
        else:
            self.node.listen(node_num)
            conn, address = self.node.accept()
            print("Connection from: " + str(address))
            while True:
                data = conn.recv(4096).decode()
                if not data:
                    break
                return data

    def connect_node(self, node, ip_address, port) -> str:
        node.settimeout(0.5)
        try:
            node.connect((ip_address, port))
        except TimeoutError:
            node.close()
        finally:
            return ip_address

    def disconnect_node(self, node) -> None:
        node.close()

    def send_message(self, node, message):
        try:
            node.send(message)
            self.requests += 1
        except OSError:
            pass

    def receive_message(self, node) -> bytes:
        response = b''
        try:
            response = node.recv(4096)
            self.responses += 1
        except OSError:
            pass
        finally:
            return response
