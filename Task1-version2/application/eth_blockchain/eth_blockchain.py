import hashlib
import random
import socket
import struct
import time
import requests
import rlp
from rlp.sedes import List, CountableList, binary, big_endian_int

from application.base_blockchain.base_blockchain import BaseBlockchain


class EthBlockchain(BaseBlockchain):
    socket: socket
    node: str
    port: int

    def __init__(self, node, port):
        super().__init__()
        self.node = node
        self.port = port

    def set_socket(self) -> socket.socket:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if str(self.socket.type) == 'SocketKind.SOCK_STREAM':
            return self.socket
        else:
            return 0

    def get_ip(self) -> str:
        ip = requests.get('https://checkip.amazonaws.com').text.strip()
        return ip

    def set_node(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 30303))

    def get_connections(self, node_number) -> tuple:
        self.socket.listen(node_number)
        while True:
            peer = self.socket.accept()
            return peer

    def connect_node(self) -> str:
        try:
            print("Trying to connect to ETH node: ", self.node)
            self.socket.connect((self.node, self.port))
            return self.node
        except Exception:
            raise Exception('Node Url invalid')

    def disconnect_node(self):
        return self.socket.close()

    def create_tx_getdata_message(self, tx_id) -> bytes:
        pass

    def create_hello_message(self):
        protocol_version = rlp.encode(66)
        client_id = rlp.encode(b"client")
        port = rlp.encode(30303)
        node_id = rlp.encode(b"b463a06c9cb44b6c5be042c931707374c9be887d91c65543aebed8d32298144b95c116b0be98a326cdef75b38726378c9fe714d2ed33e5a36c7c79ce96ca8426")
        capabilities = rlp.encode(b"eth/66")
        message = protocol_version + client_id + port + node_id + capabilities
        return message

    def create_getblocknumber_message(self):
        data = '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
        return data.encode()

    def send_message(self, message) -> int:
        return self.socket.send(message)

    def receive_message(self) -> bytes:
        return self.socket.recv(1024)


if __name__ == '__main__':
    ETH = EthBlockchain('174.1.90.30', 30303)
    ETH.set_socket()
    connection = ETH.connect_node()
    print('Connection: Node IP: ', connection)
    print('Sending Hello message request to node')
    hello_msg = ETH.create_hello_message()
    ETH.socket.sendall(hello_msg)
    print(hello_msg)
    print('Receiving response from node')
    result = ETH.receive_message()
    print(result)
