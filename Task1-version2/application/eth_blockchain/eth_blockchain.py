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
        return message.encode('utf-8')

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
        method = 'eth_getBlockByNumber'
        block_message = {
            'json': '2.0',
            'id': '0',
            'method': method,
            'params': [hex(int(block_number)), True]
        }
        return block_message

    def create_getblock_tx_number_message(self, block_number):
        method = 'eth_getBlockTransactionCountByNumber'
        block_tx_number_message = {
            'json': '2.0',
            'id': '0',
            'method': method,
            'params': [hex(int(block_number))]
        }
        return block_tx_number_message

    def create_getblock_number_message(self):
        method = 'eth_blockNumber'
        block_number_message = {
            'json': '2.0',
            'id': '0',
            'method': method,
            'params': []
        }
        return block_number_message

    def create_getnetwork_message(self):
        method = 'eth_chainId'
        network_message = {
            "jsonrpc": "2.0",
            "id": '0',
            "method": method,
            "params": [],
        }
        return network_message

    def create_mining_message(self):
        method = 'eth_mining'
        mining_message = {
            "jsonrpc": "2.0",
            "id": '0',
            "method": method,
            "params": [],
        }
        return mining_message

    def create_getbadblocks_message(self):
        method = 'debug_getBadBlocks'
        debug_message = {
            "jsonrpc": "2.0",
            "id": '0',
            "method": method,
            "params": [],
        }
        return debug_message

    def create_getgasprice_message(self):
        method = 'eth_gasPrice'
        gasprice_message = {
            "jsonrpc": "2.0",
            "id": '0',
            "method": method,
            "params": [],
        }
        return gasprice_message

    def create_ping_message(self):
        method = 'eth_syncing'
        ping_message = {
            'json': '2.0',
            'id': '0',
            'method': method,
            'params': []
        }
        return ping_message

    def encode_message(self, message):
        return message.encode('utf-8')

    def decode_message(self, response):
        response = response.decode('utf-8')
        message = {}
        status = message.update(status=response[9:15])
        type = message.update(type=response[43:47])
        time = message.update(time=str(int(response[72:74]) + 2) + response[74:80])
        length = message.update(length=len(response))
        body_start = response.find('{')
        body_end = response.rfind('}')
        body = message.update(result=json.loads(response[body_start:body_end + 1])['result'])
        return json.dumps(message, indent=4)

    def print_response(self, command, request_data, response_data) -> None:
        print("")
        print(f"Message: {command}")
        print("Program Request:")
        print(request_data)
        print("Node response:")
        print(response_data)

    def send_message(self, message) -> int:
        return self.socket.send(message)

    def receive_message(self) -> bytes:
        return self.socket.recv(4096)


if __name__ == '__main__':
    print('Interface for manual node connection to ETH Blockchain network')
    node = '89.117.58.225'
    port = 8545
    ETH = EthBlockchain(node, port)
    print('Socket info: ', ETH.set_socket())
    connection = ETH.connect_node()
    request = ETH.make_message(node, ETH.create_getgasprice_message())
    ETH.send_message(request)
    response = ETH.receive_message()
    response = ETH.decode_message(response)
    ETH.print_response('Gas Price', request, response)
    # print("Get mining status message")
    # message6 = ETH.make_message(node, ETH.create_getbadblocks_message())
    # request = ETH.encode_message(message6)
    # ETH.send_message(request)
    # print(f'Request:\n{request}')
    # response = ETH.receive_message().decode('utf-8')
    # print(f'Response:\n{response}')
    # print("Get network message")
    # message5 = ETH.make_message(node, ETH.create_getnetwork_message())
    # request = ETH.encode_message(message5)
    # ETH.send_message(request)
    # print(f'Request:\n{request}')
    # response = ETH.receive_message().decode('utf-8')
    # print(f'Response:\n{response}')
    # message4 = ETH.make_message(node, ETH.create_ping_message())
    # request = ETH.encode_message(message4)
    # ETH.send_message(request)
    # print(f'Request:\n{request}')
    # response = ETH.receive_message().decode('utf-8')
    # print(f'Response:\n{response}')
    # print("Get block tx number message")
    # message3 = ETH.make_message(node, ETH.create_getblock_tx_number_message(1))
    # request = ETH.encode_message(message3)
    # ETH.send_message(request)
    # print(f'Request:\n{request}')
    # response = ETH.receive_message().decode('utf-8')
    # print(f'Response:\n{response}')
    # print("Get block message")
    # message2 = ETH.make_message(node, ETH.create_getblock_message(100))
    # request = ETH.encode_message(message2)
    # ETH.send_message(request)
    # print(f'Request:\n{request}')
    # response = ETH.receive_message().decode('utf-8')
    # print(f'Response:\n{response}')
    # print("Get tx data message")
    # message2 = ETH.make_message(node, ETH.create_tx_getdata_message('0xb5c8bd9430b6cc87a0e2fe110ece6bf527fa4f170a4bc8cd032f768fc5219838'))
    # request = ETH.encode_message(message2)
    # ETH.send_message(request)
    # print(f'Request:\n{request}')
    # response = ETH.receive_message().decode('utf-8')
    # print(f'Response:\n{response}')
