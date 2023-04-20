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

    def handle_getaddr_response(self):
        pass
