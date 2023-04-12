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

    def make_message(self, command, payload):
        request_command = f"{command} / HTTP/1.1\r\n"
        host = f"Host: {host_ip}\r\n"
        content_type = f"Content-Type: application/json\r\n"
        content_length = f"Content-Length: {len(json.dumps(payload))}\r\n\r\n{json.dumps(payload)}"
        message = request_command + host + content_type + content_length

        return message.encode('utf-8')

    def create_getdata_message(self, tx_id):
        command = 'eth_getTransactionByHash'
        tx_getdata_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [tx_id],
            'id': json_id
        }

        return tx_getdata_message

    def create_getblock_message(self, block_number):
        command = 'eth_getBlockByNumber'
        block_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [hex(block_number), False],
            'id': json_id
        }

        return block_message

    def create_getblock_tx_number_message(self, block_number):
        command = 'eth_getBlockTransactionCountByNumber'
        block_tx_number_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [hex(block_number)],
            'id': json_id
        }

        return block_tx_number_message

    def create_best_block_height_message(self):
        command = 'eth_blockNumber'
        best_block_height_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [],
            'id': json_id,
        }

        return best_block_height_message

    def create_getnetwork_message(self):
        command = 'eth_chainId'
        network_message = {
            "jsonrpc": json_version,
            "method": command,
            "params": [],
            "id": json_id
        }

        return network_message

    def create_getmining_message(self):
        command = 'eth_mining'
        mining_message = {
            "jsonrpc": json_version,
            "method": command,
            "params": [],
            "id": json_id
        }

        return mining_message

    def create_getbadblocks_message(self):
        command = 'debug_getBadBlocks'
        debug_bad_blocks_message = {
            "jsonrpc": json_version,
            "method": command,
            "params": [],
            "id": json_id
        }

        return debug_bad_blocks_message

    def create_getgasprice_message(self):
        command = 'eth_gasPrice'
        gas_price_message = {
            "jsonrpc": json_version,
            "method": command,
            "params": [],
            "id": json_id
        }

        return gas_price_message

    def create_ping_message(self):
        command = 'eth_syncing'
        ping_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [],
            'id': json_id
        }

        return ping_message

    def create_hashrate_message(self):
        command = 'eth_hashrate'
        hashrate_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [],
            'id': json_id
        }

        return hashrate_message

    def create_net_listening_payload():
        command = 'net_listening'
        net_listening_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [],
            'id': json_id
        }

        return net_listening_message

    def send_message(self, message) -> int:
        return self.socket.send(message)

    def receive_message(self) -> bytes:
        return self.socket.recv(4096)

    def decode_response_message(self, response):
        response = response.decode('utf-8')
        message = {}
        status = message['status'] = response[9:15]
        type = message['type'] = response[43:47]
        length = message.update(length=len(response))
        body_start = response.find('{')
        if 'transactions' in response:
            body_end = response.rfind('transactions')
            response = response[body_start:body_end - 2] + '}' + '}'
            message.update(result=json.loads(response)['result'])
        else:
            body_end = response.rfind('}')
            message.update(result=json.loads(response[body_start:body_end + 1])['result'])

        return message

