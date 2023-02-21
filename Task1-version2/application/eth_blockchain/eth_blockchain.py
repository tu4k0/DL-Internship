import hashlib
import random
import socket
import struct
import time
import requests

from application.base_blockchain.base_blockchain import BaseBlockchain


class EthBlockchain(BaseBlockchain):
    socket: socket

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
        self.socket.bind(('', 8546))

    def get_connections(self, node_number) -> tuple:
        self.socket.listen(node_number)
        while True:
            peer = self.socket.accept()
            return peer

    def connect_node(self, node, port) -> str:
        try:
            print("Trying to connect to BTC node: ", node)
            self.socket.connect((node, port))
            return node
        except Exception:
            raise Exception('Node Url invalid')

    def disconnect_node(self):
        return self.socket.close()

    def create_tx_getdata_message(self, tx_id) -> bytes:
        pass

    def get_block_number(self):
        data = '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
        return data.encode()

    def send_message(self, message) -> int:
        return self.socket.send(message)

    def receive_message(self) -> bytes:
        return self.socket.recv(1024)


if __name__ == '__main__':
    ETH = EthBlockchain('136.243.110.222', 30033)
    ETH.set_socket()
    ETH.connect_node('136.243.110.222', 30033)
    ETH.send_message(ETH.get_block_number())
    result = ETH.receive_message()
    print(result)
