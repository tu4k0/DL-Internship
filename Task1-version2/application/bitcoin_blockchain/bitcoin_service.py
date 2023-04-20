import binascii
import requests

from application.base_blockchain.base_blockchain import BaseBlockchain


class BitcoinService(BaseBlockchain):

    def handle_getheaders_response(self, response) -> str:
        index = str(response).find("getheaders")
        if index == -1:
            getheaders = self.receive_message()
            index = str(getheaders).find("getheaders")
            header = binascii.hexlify(getheaders)[index + 40:index + 104]
        else:
            header = binascii.hexlify(response)[140:204]

        block = header.decode("utf-8")
        block_hash = bytearray.fromhex(block)
        block_hash.reverse()

        return block_hash.hex()

    def handle_block_height(self, block_hash):
        block_height_message = f"https://blockstream.info/api/block/{block_hash}"
        response = requests.get(block_height_message)
        block_height = response.json()['height']

        return block_height

    def handle_getaddr_response(self, response, node_number):
        found_peers = []
        found_nodes = {}
        search_index = 0
        getaddr_index = str(response).find("addr")
        if getaddr_index != -1:
            response_data = self.receive_message()[3:]
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
