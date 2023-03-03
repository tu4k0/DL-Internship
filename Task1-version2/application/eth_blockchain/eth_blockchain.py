import hashlib
import random
import socket
import struct
import time
import requests
import rlp
import json

from rlp.sedes import List, CountableList, binary, big_endian_int

from application.base_blockchain.base_blockchain import BaseBlockchain


class EthBlockchain(BaseBlockchain):
    socket: socket
    node: str
    port: int

    def __init__(self, node, port):
        super().__init__()
        self.node = node
        self.port = int(port)

    def set_socket(self) -> socket.socket:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self.socket

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

    def make_message(self, node, message):
        request_method = "POST / HTTP/1.1\r\n"
        host = f"Host: {node}\r\n"
        content_type = f"Content-Type: application/json\r\n"
        content_length = f"Content-Length: {len(json.dumps(message))}\r\n\r\n{json.dumps(message)}"
        message = request_method + host + content_type + content_length
        return message

    def create_tx_getdata_message(self, tx_id) -> bytes:
        method = 'eth_getTransactionByHash'
        tx_getdata_message = {
            'json': '2.0',
            'id': '0',
            'method': method,
            'params': [tx_id]
        }
        return tx_getdata_message

    def create_getblock_message(self, block_number) -> bytes:
        method = 'eth_getBlockByHash'
        getblock_message = {
            'json': '2.0',
            'id': '0',
            'method': method,
            'params': [
                hex(int(block_number)), True]
        }
        return getblock_message

    def create_getblocknumber_message(self):
        method = 'eth_blockNumber'
        getblocknumber_message = {
            'json': '2.0',
            'id': '0',
            'method': method,
            'params': []
        }
        return getblocknumber_message

    def encode_message(self, message):
        return message.encode('utf-8')

    def send_message(self, message) -> int:
        return self.socket.send(message)

    def receive_message(self) -> bytes:
        return self.socket.recv(1024)


if __name__ == '__main__':
    print('Interface for manual node connection to ETH Blockchain network')
    node = '144.217.253.194'
    port = 8545
    ETH = EthBlockchain(node, port)
    print('Socket info: ', ETH.set_socket())
    connection = ETH.connect_node()
    print("Get tx data message")
    message2 = ETH.make_message(node, ETH.create_getblock_message(
        '1222'))
    request = ETH.encode_message(message2)
    ETH.send_message(request)
    print(f'Request:\n{request}')
    response = ETH.receive_message().decode('utf-8')
    print(f'Response:\n{response}')
    # print("Get tx data message")
    # message2 = ETH.make_message(node, ETH.create_tx_getdata_message('0xb5c8bd9430b6cc87a0e2fe110ece6bf527fa4f170a4bc8cd032f768fc5219838'))
    # request = ETH.encode_message(message2)
    # ETH.send_message(request)
    # print(f'Request:\n{request}')
    # response = ETH.receive_message().decode('utf-8')
    # print(f'Response:\n{response}')
