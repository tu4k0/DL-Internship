import socket
import requests

from abc import abstractmethod, ABC
from application.btc_blockchain.btc_config import *
from application.eth_blockchain.eth_config import *


class BaseBlockchain(ABC):
    socket: socket
    node: socket
    ip_address: str
    port: int

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def make_message(self, command, payload) -> bytes | str:
        pass

    @abstractmethod
    def create_getdata_message(self, tx_id):
        pass

    @abstractmethod
    def create_ping_message(self):
        pass

    @abstractmethod
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
        try:
            self.ip_address = str(ip_address)
            self.port = int(port)
            self.socket.connect((self.ip_address, self.port))
            return self.ip_address
        except Exception:
            raise Exception('Node Url invalid')

    def disconnect_node(self) -> None:
        self.socket.close()

    def send_message(self, message) -> int:
        return self.socket.send(message)

    def receive_message(self) -> bytes:
        return self.socket.recv(4096)

    def print_response(self, command, request_message, response_message) -> None:
        print("")
        print(f"Message: {command}")
        print("Program Request:")
        print(request_message)
        print("Node response:")
        print(self.decode_response_message(response_message))