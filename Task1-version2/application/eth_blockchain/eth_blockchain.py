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

    def create_tx_getdata_message(self, tx_id) -> bytes:
        pass

    def create_status_message(self):
        msg_type = 0x00
        protocol_version = 66
        network_id = 1
        td = 58750003716598360000000
        blockhash = bytes.fromhex('c68967de7c192d63fb1387ea15a77294e5c832b394a95cd24bddb48fb96d620f')
        genesis = bytes.fromhex('d4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3')
        fork_hash = bytes.fromhex('97c2c34c')
        fork_next = 10
        fork_id = [fork_hash, fork_next]
        status_payload = rlp.encode([protocol_version, network_id, td, blockhash, genesis, fork_id])
        header = msg_type.to_bytes(1, byteorder='big') + len(status_payload).to_bytes(3, byteorder='big')
        message = header + status_payload
        return message

    def create_hello_message(self):
        protocol_version = 5
        client_id = 'geth/v1.10.25-stable/linux-amd64/go1.19'
        listen_port = 30303
        node_id = '003b78a323c5c0d348b7ab4411ee72faa3733cf0e9c0b339719f8f94fcd81cdacdca2f89520392b4c86b561b738bf10b76d28db1dae070be035bb6c1c7e43e14'
        capabilities = [['eth', 66]]
        hello_message = rlp.encode([protocol_version, client_id, capabilities, listen_port, node_id])
        return hello_message

    def create_getblocknumber_message(self):
        data = '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
        return data.encode()

    def send_message(self, message) -> int:
        return self.socket.send(message)

    def receive_message(self) -> bytes:
        return self.socket.recv(1024)


if __name__ == '__main__':
    ETH = EthBlockchain('89.116.26.40', 30303)
    ETH.set_socket()
    connection = ETH.connect_node()
    print('Connection: Node IP: ', connection)
    print('Sending Hello message request to node')
    hello_msg = ETH.create_hello_message()
    ETH.socket.send(hello_msg)
    print(hello_msg)
    print('Receiving response from node')
    response = ETH.receive_message()
    print(response)
    print('Sending Status message request to node')
    status_msg = ETH.create_status_message()
    ETH.socket.sendall(status_msg)
    print(status_msg)
    print('Receiving response from node')
    result = ETH.receive_message()
    print(result)

