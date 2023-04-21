import binascii
import requests

from application.bitcoin_blockchain.bitcoin import Bitcoin
from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P


class BitcoinService:
    bitcoin: Bitcoin
    bitcoin_p2p: BitcoinP2P

    def __init__(self, user_request):
        self.bitcoin = Bitcoin(ip_address=user_request[0], port=user_request[1], node_number=user_request[2])
        self.bitcoin_p2p = BitcoinP2P()

    def start_session(self, user_request):
        ip_address = user_request[0]
        port = user_request[1]
        node_number = user_request[2]
        self.bitcoin_p2p.set_socket()
        connection = self.bitcoin_p2p.connect_node(ip_address, port)
        if connection:
            print("active connections: ", node_number)
            version_payload = self.bitcoin_p2p.create_version_payload(ip_address)
            version_message = self.bitcoin_p2p.create_message('version', version_payload)
            verack_message = self.bitcoin_p2p.create_verack_payload()
            getdata_payload = self.bitcoin_p2p.create_getdata_payload()
            getdata_message = self.bitcoin_p2p.create_message('getdata', getdata_payload)
            self.bitcoin_p2p.send_message(version_message)
            self.bitcoin_p2p.receive_message()
            self.bitcoin_p2p.send_message(verack_message)
            self.bitcoin_p2p.receive_message()
            self.bitcoin_p2p.send_message(getdata_message)
            self.bitcoin_p2p.receive_message()
            response_data = self.bitcoin_p2p.receive_message()
            best_block_hash, prev_block_hash = self.presenter_getheaders_response(response_data)
            best_block_number = self.presenter_block_height(best_block_hash)
            prev_block_number = self.presenter_block_height(prev_block_hash)
            self.bitcoin.best_block_height = best_block_number
            self.bitcoin.best_block_hash = best_block_hash
            self.bitcoin.previous_block_height = prev_block_number
            self.bitcoin.previous_block_hash = prev_block_hash
            self.bitcoin.amount_sent_messages = self.bitcoin_p2p.requests
            self.bitcoin.amount_received_messages = self.bitcoin_p2p.responses

    def presenter_getheaders_response(self, response):
        index = str(response).find("getheaders")
        if index == -1:
            getheaders = self.bitcoin_p2p.receive_message()
            index = str(getheaders).find("getheaders")
            best_block = binascii.hexlify(getheaders)[index + 40:index + 104]
            prev_block_hash = binascii.hexlify(getheaders)[index + 104:index + 104 + 64].decode("utf-8")
        else:
            best_block = binascii.hexlify(response)[140:204]
            prev_block_hash = binascii.hexlify(response)[204:268].decode("utf-8")

        best_block_hash = best_block.decode("utf-8")
        best_block_hash = bytearray.fromhex(best_block_hash)
        best_block_hash.reverse()
        prev_block_hash = bytearray.fromhex(prev_block_hash)
        prev_block_hash.reverse()

        return best_block_hash.hex(), prev_block_hash.hex()

    def presenter_block_height(self, block_hash):
        block_height = 0
        while block_height == 0:
            block_height_message = f"https://blockstream.info/api/block/{block_hash}"
            response = requests.get(block_height_message)
            response.raise_for_status()
            if response.status_code != 204:
                block_height = response.json()['height']

        return block_height

    def handle_getaddr_response(self, response, node_number):
        found_peers = []
        found_nodes = {}
        search_index = 0
        getaddr_index = str(response).find("addr")
        if getaddr_index != -1:
            response_data = self.bitcoin_p2p.receive_message()[3:]
            nodes = binascii.hexlify(response_data)
            node_info_size = 60
            while len(found_nodes) < node_number:
                found_peers.append(nodes[:node_info_size])
                node_index = str(found_peers[search_index]).rfind("ffff")
                if node_index != -1:
                    nodes = nodes[node_info_size:]
                    found = found_peers[search_index][node_index + 2:node_index + 14]
                    ip_address_hex = found[:8]
                    port = int(found[8:12], 16)
                    if port == 8333:
                        ip_address = ''
                        for i in range(0, len(ip_address_hex), 2):
                            ip_address_dec = int(ip_address_hex[i:i + 2], 16)
                            ip_address += f'{ip_address_dec}.'
                        search_index += 1
                        found_nodes.update({ip_address.rstrip('.'): port})
                    else:
                        pass
                else:
                    nodes = nodes[node_info_size:]
            return found_nodes

    def close_session(self):
        self.bitcoin_p2p.disconnect_node()
