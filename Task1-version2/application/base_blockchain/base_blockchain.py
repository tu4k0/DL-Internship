import socket
import requests

from abc import abstractmethod, ABC
from application.bitcoin_blockchain.bitcoin_config import *
from application.ethereum_blockchain.eth_config import *


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
    def create_getdata_payload(self):
        pass

    @abstractmethod
    def create_ping_payload(self):
        pass

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

    def connect_node(self, node, ip_address, port) -> str:
        node.settimeout(2)
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

    def receive_message(self, node):
        response = b''
        try:
            response = node.recv(4096)
            self.responses += 1
        except OSError:
            pass
        finally:
            return response
