import binascii
import requests

from application.bitcoin_blockchain.bitcoin import Bitcoin
from application.bitcoin_blockchain.bitcoin_config import BITCOIN_GETHEADERS_COMMAND_HEX
from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P
from application.multithreading.base_thread import BaseThread


class BitcoinNodeThread(BaseThread):
    ip: str
    port: int
    bitcoin: Bitcoin
    bitcoin_p2p: BitcoinP2P

    def __init__(self, ip_address: str, port: int, bitcoin: Bitcoin, bitcoin_p2p: BitcoinP2P):
        super().__init__()
        self.ip = ip_address
        self.port = port
        self.bitcoin = bitcoin
        self.bitcoin_p2p = bitcoin_p2p

    def run(self):
        node = self.bitcoin_p2p.set_socket()
        connection = self.bitcoin_p2p.connect_node(node, self.ip, self.port)
        if connection:
            version_payload = self.bitcoin_p2p.create_version_payload(self.ip)
            version_message = self.bitcoin_p2p.create_message('version', version_payload)
            verack_payload = self.bitcoin_p2p.create_verack_payload()
            verack_message = self.bitcoin_p2p.create_message('verack', verack_payload)
            getdata_payload = self.bitcoin_p2p.create_getdata_payload()
            getdata_message = self.bitcoin_p2p.create_message('getdata', getdata_payload)
            self.bitcoin_p2p.send_message(node, version_message)
            version_response = self.bitcoin_p2p.receive_message(node)
            if not version_response:
                best_block_hash = None
                best_block_number = None
                prev_block_number = None
                prev_block_hash = None
                self.bitcoin.best_block_hashes.append(best_block_hash)
                self.bitcoin.best_block_numbers.append(best_block_number)
                self.bitcoin.prev_block_hashes.append(prev_block_hash)
                self.bitcoin.prev_block_numbers.append(prev_block_number)
            else:
                self.bitcoin.active_connections += 1
                self.bitcoin_p2p.send_message(node, verack_message)
                response_data = self.bitcoin_p2p.receive_message(node)
                self.bitcoin_p2p.send_message(node, getdata_message)
                while True:
                    if str(response_data).find('getheaders') != -1:
                        best_block_hash, prev_block_hash = self.handle_getheaders_message(node, response_data)
                        break
                    else:
                        response_data = self.bitcoin_p2p.receive_message(node)
                best_block_number = self.get_best_block_height(best_block_hash)
                self.bitcoin.best_block_hashes.append(best_block_hash)
                self.bitcoin.best_block_numbers.append(best_block_number)
                self.bitcoin.prev_block_numbers.append(best_block_number - 1)
                self.bitcoin.prev_block_hashes.append(prev_block_hash)
            node.close()

    def handle_getheaders_message(self, node, response_data) -> tuple[str, str]:
        getheaders = binascii.hexlify(response_data)
        getheaders_index = str(getheaders).find(BITCOIN_GETHEADERS_COMMAND_HEX)
        if len(getheaders[getheaders_index - 2:]) == 40:
            response_data += self.bitcoin_p2p.receive_message(node)
        info = binascii.hexlify(response_data)
        index = str(info).find(BITCOIN_GETHEADERS_COMMAND_HEX)
        starting_hash = str(info)[index + 50:]
        block_hash_size = 64
        block_hashes = []
        start_hash_index = 0
        for i in range(1, 3):
            block_hashes.append(starting_hash[start_hash_index:block_hash_size])
            start_hash_index += 64
            block_hash_size += 64
        best_block_hash = bytearray.fromhex(block_hashes[0])
        best_block_hash.reverse()
        prev_block_hash = bytearray.fromhex(block_hashes[1])
        prev_block_hash.reverse()

        return best_block_hash.hex(), prev_block_hash.hex()

    def get_best_block_height(self, block_hash) -> int:
        block_height = 0
        while block_height == 0:
            block_height_message = f"https://blockstream.info/api/block/{block_hash}"
            response = requests.get(block_height_message)
            response.raise_for_status()
            if response.status_code != 204:
                block_height = response.json()['height']

        return block_height
