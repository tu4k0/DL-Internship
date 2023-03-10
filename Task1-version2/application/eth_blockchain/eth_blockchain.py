import socket
import struct
import time
import requests
import rlp
import json

from application.base_blockchain.base_blockchain import BaseBlockchain
from application.eth_blockchain.eth_config import *


class EthBlockchain(BaseBlockchain):
    ip_address: str
    port: int
    socket: socket
    node: socket

    def __init__(self):
        super().__init__()

    def set_node(self):
        super().set_node()
        self.node.bind(('', eth_mainnet_port))

        return self.node

    def make_message(self, node, message):
        request_method = "POST / HTTP/1.1\r\n"
        host = f"Host: {node}\r\n"
        content_type = f"Content-Type: application/json\r\n"
        content_length = f"Content-Length: {len(json.dumps(message))}\r\n\r\n{json.dumps(message)}"
        message = request_method + host + content_type + content_length

        return message.encode('utf-8')

    def create_getdata_message(self, tx_id) -> bytes:
        method = 'eth_getTransactionByHash'
        tx_getdata_message = {
            'json': json_version,
            'id': '0',
            'method': method,
            'params': [tx_id]
        }

        return tx_getdata_message

    def create_getblock_message(self, block_number) -> bytes:
        method = 'eth_getBlockByNumber'
        block_message = {
            'json': json_version,
            'id': json_id,
            'method': method,
            'params': [hex(int(block_number)), True]
        }

        return block_message

    def create_getblock_tx_number_message(self, block_number):
        method = 'eth_getBlockTransactionCountByNumber'
        block_tx_number_message = {
            'json': json_version,
            'id': json_id,
            'method': method,
            'params': [hex(int(block_number))]
        }

        return block_tx_number_message

    def create_getblock_number_message(self):
        method = 'eth_blockNumber'
        block_number_message = {
            'json': json_version,
            'id': json_id,
            'method': method,
            'params': []
        }

        return block_number_message

    def create_getnetwork_message(self):
        method = 'eth_chainId'
        network_message = {
            "jsonrpc": json_version,
            "id": json_id,
            "method": method,
            "params": [],
        }

        return network_message

    def create_getmining_message(self):
        method = 'eth_mining'
        mining_message = {
            "jsonrpc": json_version,
            "id": json_id,
            "method": method,
            "params": [],
        }

        return mining_message

    def create_getbadblocks_message(self):
        method = 'debug_getBadBlocks'
        debug_message = {
            "jsonrpc": json_version,
            "id": json_id,
            "method": method,
            "params": [],
        }

        return debug_message

    def create_getgasprice_message(self):
        method = 'eth_gasPrice'
        gasprice_message = {
            "jsonrpc": json_version,
            "id": json_id,
            "method": method,
            "params": [],
        }

        return gasprice_message

    def create_ping_message(self):
        method = 'eth_syncing'
        ping_message = {
            'json': json_version,
            'id': json_id,
            'method': method,
            'params': []
        }

        return ping_message

    def send_message(self, message) -> int:
        return self.socket.send(message)

    def receive_message(self) -> bytes:
        return self.socket.recv(4096)

    def decode_response_message(self, response):
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

