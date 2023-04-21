import csv
import socket
import json

from application.base_blockchain.base_blockchain import BaseBlockchain
from application.ethereum_blockchain.eth_config import *


class EthereumP2P(BaseBlockchain):
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

    def get_nodes(self, nodes_list, node_number):
        with open(nodes_list, 'r') as nodes:
            nodes = csv.reader(nodes)
            found_peers = dict()
            search_index = 0
            for node_info in nodes:
                if search_index == node_number + 1:
                    break
                else:
                    if search_index == 0:
                        search_index += 1
                    else:
                        found_peers.update({node_info[2]: 8545})
                        search_index += 1

        return found_peers

    def make_message(self, payload):
        request_method = "POST / HTTP/1.1\r\n"
        host = f"Host: {host_ip}\r\n"
        content_type = f"Content-Type: application/json\r\n"
        content_length = f"Content-Length: {len(json.dumps(payload))}\r\n\r\n{json.dumps(payload)}"
        message = request_method + host + content_type + content_length

        return message.encode('utf-8')

    def create_getdata_payload(self, tx_id):
        command = 'eth_getTransactionByHash'
        tx_getdata_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [tx_id],
            'id': json_id
        }

        return tx_getdata_message

    def create_getblock_by_number_payload(self, block_number):
        command = 'eth_getBlockByNumber'
        block_number_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [hex(block_number), False],
            'id': json_id
        }

        return block_number_message

    def create_getblock_by_hash_payload(self, block_hash):
        command = 'eth_getBlockByHash'
        block_hash_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [block_hash, False],
            'id': json_id
        }

        return block_hash_message

    def create_getblock_tx_number_payload(self, block_number):
        command = 'eth_getBlockTransactionCountByNumber'
        block_tx_number_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [hex(block_number)],
            'id': json_id
        }

        return block_tx_number_message

    def create_get_tx_by_hash_payload(self, tx_hash):
        command = 'eth_getTransactionByHash'
        tx_hash_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [tx_hash],
            'id': json_id
        }

        return tx_hash_message

    def create_best_block_height_payload(self):
        command = 'eth_blockNumber'
        best_block_height_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [],
            'id': json_id,
        }

        return best_block_height_message

    def create_getnetwork_payload(self):
        command = 'eth_chainId'
        network_message = {
            "jsonrpc": json_version,
            "method": command,
            "params": [],
            "id": json_id
        }

        return network_message

    def create_getmining_payload(self):
        command = 'eth_mining'
        mining_message = {
            "jsonrpc": json_version,
            "method": command,
            "params": [],
            "id": json_id
        }

        return mining_message

    def create_getbadblocks_payload(self):
        command = 'debug_getBadBlocks'
        debug_bad_blocks_message = {
            "jsonrpc": json_version,
            "method": command,
            "params": [],
            "id": json_id
        }

        return debug_bad_blocks_message

    def create_getgasprice_payload(self):
        command = 'eth_gasPrice'
        gas_price_message = {
            "jsonrpc": json_version,
            "method": command,
            "params": [],
            "id": json_id
        }

        return gas_price_message

    def create_ping_payload(self):
        command = 'eth_syncing'
        ping_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [],
            'id': json_id
        }

        return ping_message

    def create_hashrate_payload(self):
        command = 'eth_hashrate'
        hashrate_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [],
            'id': json_id
        }

        return hashrate_message

    def create_net_listening_payload(self):
        command = 'net_listening'
        net_listening_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [],
            'id': json_id
        }

        return net_listening_message

    def create_net_peer_count_payload(self):
        command = 'net_peerCount'
        net_peer_count_message = {
            'jsonrpc': json_version,
            'method': command,
            'params': [],
            'id': json_id
        }

        return net_peer_count_message
