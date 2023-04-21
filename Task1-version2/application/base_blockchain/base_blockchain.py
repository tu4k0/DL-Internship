import socket
import requests

from abc import abstractmethod, ABC
from application.bitcoin_blockchain.bitcoin_config import *
from application.eth_blockchain.eth_config import *


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
    def create_message(self, command, payload) -> bytes or str:
        pass

    @abstractmethod
    def create_getdata_payload(self):
        pass

    @abstractmethod
    def create_ping_payload(self):
        pass

    # abstract method
    def decode_response_message(self, response_message):
        pass

    def get_ip(self) -> str:
        ip = requests.get(ip_link).text.strip()

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
                data = conn.recv(1024).decode()
                if not data:
                    break
                return data

    def connect_node(self, ip_address, port) -> str:
        self.ip_address = str(ip_address)
        self.port = int(port)
        try:
            self.socket.connect((self.ip_address, self.port))
        except TimeoutError:
            self.socket.close()
        finally:
            return self.ip_address

    def disconnect_node(self) -> None:
        self.socket.close()

    def send_message(self, message) -> int:
        try:
            self.requests += 1
            return self.socket.send(message)
        except OSError:
            pass

    def receive_message(self) -> bytes:
        try:
            self.responses += 1
            return self.socket.recv(4096)
        except OSError:
            pass

    def print_response(self, command, request_message, response_message) -> None:
        print(f"Message: {command}")
        print("Request:")
        print(request_message)
        print("Response:")
        print(response_message)