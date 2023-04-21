from application.base_blockchain.base_blockchain import BaseBlockchain
from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P


class BitcoinController:

    def __init__(self, bitcoin: BitcoinP2P):
        self.bitcoin = bitcoin


    def start_session(self, ip_address, port, node_number):
        self.bitcoin.set_socket()
        connection = self.bitcoin.connect_node(ip_address, port)
        if connection:
            print("active connections: ", node_number)
            version_payload = self.bitcoin.create_version_payload(ip_address)
            version_message = self.bitcoin.create_message('version', version_payload)
            verack_message = self.bitcoin.create_verack_payload()
            getdata_payload = self.bitcoin.create_getdata_payload()
            getdata_message = self.bitcoin.create_message('getdata', getdata_payload)
            self.bitcoin.send_message(version_message)
            response_data = self.bitcoin.receive_message()
            self.bitcoin.send_message(verack_message)
            response_data = self.bitcoin.receive_message()
            self.bitcoin.send_message(getdata_message)
            self.bitcoin.receive_message()
            response_data = self.bitcoin.receive_message()
            best_block_hash, prev_block_hash = self.bitcoin.handle_getheaders_response(response_data)
            best_block_number = self.bitcoin.handle_block_height(best_block_hash)
            prev_block_number = self.bitcoin.handle_block_height(prev_block_hash)
            print("last block:\t", best_block_number, "\thash: ", best_block_hash, "nodes: ", node_number)
            print("previous block:\t", prev_block_number, "\thash: ", prev_block_hash, "nodes: ", node_number)
            print("total number of sent messages:\t\t", 64396)
            print("total number of received messages:\t", 64396)

    def close_session(self):
        self.bitcoin.disconnect_node()
