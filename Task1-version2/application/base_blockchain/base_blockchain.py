import socket
import requests

from abc import abstractmethod, ABC


class BaseBlockchain(ABC):
    socket: socket
    ip_address: str
    port: int
    requests: int
    responses: int

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

    def connect(self, node: socket.socket, ip_address: str, port: int) -> str:
        node.settimeout(0.5)
        try:
            node.connect((ip_address, port))
        except TimeoutError:
            node.close()
        finally:
            return ip_address

    def disconnect(self, node: socket.socket) -> None:
        node.close()

    def send_message(self, node: socket.socket, message: str | bytes):
        try:
            self.requests += 1
            node.send(message)
        except OSError:
            pass

    def receive_message(self, node: socket.socket) -> bytes:
        response = b''
        try:
            response = node.recv(4096)
            self.responses += 1
        except OSError:
            pass
        finally:
            return response
