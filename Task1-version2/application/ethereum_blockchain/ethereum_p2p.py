import json
import socket

from application.base_blockchain.base_blockchain import BaseBlockchain
from application.ethereum_blockchain.ethereum_config import HOST, ETHEREUM_MAINNET_PORT, JSON_VERSION, JSON_ID


class EthereumP2P(BaseBlockchain):
    ip_address: str
    port: int
    socket: socket
    node: socket

    def __init__(self):
        super().__init__()

    def set_node(self):
        super().set_node()
        self.node.bind(('', ETHEREUM_MAINNET_PORT))

        return self.node

    def create_message(self, payload) -> bytes:
        request_method = f"POST / HTTP/1.1\r\n"
        host = f"Host: {HOST}\r\n"
        content_type = f"Content-Type: application/json\r\n"
        content_length = f"Content-Length: {len(json.dumps(payload))}\r\n\r\n{json.dumps(payload)}"
        message = (request_method + host + content_type + content_length).encode('utf-8')

        return message

    def create_getdata_payload(self, tx_id) -> dict[str, str | list]:
        command = 'eth_getTransactionByHash'
        tx_getdata_message = {
            'jsonrpc': JSON_VERSION,
            'method': command,
            'params': [tx_id],
            'id': JSON_ID
        }

        return tx_getdata_message

    def create_getblock_by_number_payload(self, block_number) -> dict[str, str | list]:
        command = 'eth_getBlockByNumber'
        block_number_message = {
            'jsonrpc': JSON_VERSION,
            'method': command,
            'params': [hex(int(block_number)), False],
            'id': JSON_ID
        }

        return block_number_message

    def create_getblock_by_hash_payload(self, block_hash) -> dict[str, str | list]:
        command = 'eth_getBlockByHash'
        block_hash_message = {
            'jsonrpc': JSON_VERSION,
            'method': command,
            'params': [block_hash, False],
            'id': JSON_ID
        }

        return block_hash_message

    def create_getblock_tx_number_payload(self, block_number) -> dict[str, str | list]:
        command = 'eth_getBlockTransactionCountByNumber'
        block_tx_number_message = {
            'jsonrpc': JSON_VERSION,
            'method': command,
            'params': [hex(block_number)],
            'id': JSON_ID
        }

        return block_tx_number_message

    def create_get_tx_by_hash_payload(self, tx_hash) -> dict[str, str | list]:
        command = 'eth_getTransactionByHash'
        tx_hash_message = {
            'jsonrpc': JSON_VERSION,
            'method': command,
            'params': [tx_hash],
            'id': JSON_ID
        }

        return tx_hash_message

    def create_best_block_height_payload(self) -> dict[str, str | list]:
        command = 'eth_blockNumber'
        best_block_height_message = {
            'jsonrpc': JSON_VERSION,
            'method': command,
            'params': [],
            'id': JSON_ID,
        }

        return best_block_height_message

    def create_getnetwork_payload(self) -> dict[str, str | list]:
        command = 'eth_chainId'
        network_message = {
            "jsonrpc": JSON_VERSION,
            "method": command,
            "params": [],
            "id": JSON_ID
        }

        return network_message

    def create_getmining_payload(self) -> dict[str, str | list]:
        command = 'eth_mining'
        mining_message = {
            "jsonrpc": JSON_VERSION,
            "method": command,
            "params": [],
            "id": JSON_ID
        }

        return mining_message

    def create_getbadblocks_payload(self) -> dict[str, str | list]:
        command = 'debug_getBadBlocks'
        debug_bad_blocks_message = {
            "jsonrpc": JSON_VERSION,
            "method": command,
            "params": [],
            "id": JSON_ID
        }

        return debug_bad_blocks_message

    def create_getgasprice_payload(self) -> dict[str, str | list]:
        command = 'eth_gasPrice'
        gas_price_message = {
            "jsonrpc": JSON_VERSION,
            "method": command,
            "params": [],
            "id": JSON_ID
        }

        return gas_price_message

    def create_syncing_payload(self) -> dict[str, str | list]:
        command = 'eth_syncing'
        ping_message = {
            'jsonrpc': JSON_VERSION,
            'method': command,
            'params': [],
            'id': JSON_ID
        }

        return ping_message

    def create_hashrate_payload(self) -> dict[str, str | list]:
        command = 'eth_hashrate'
        hashrate_message = {
            'jsonrpc': JSON_VERSION,
            'method': command,
            'params': [],
            'id': JSON_ID
        }

        return hashrate_message

    def create_ping_payload(self) -> dict[str, str | list]:
        command = 'net_listening'
        net_listening_message = {
            'jsonrpc': JSON_VERSION,
            'method': command,
            'params': [],
            'id': JSON_ID
        }

        return net_listening_message

    def create_net_peer_count_payload(self) -> dict[str, str | list]:
        command = 'net_peerCount'
        net_peer_count_message = {
            'jsonrpc': JSON_VERSION,
            'method': command,
            'params': [],
            'id': JSON_ID
        }

        return net_peer_count_message
