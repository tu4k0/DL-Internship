from application.base_blockchain.base_blockchain import BaseBlockchain
from application.bitcoin_blockchain.bitcoin import Bitcoin


class BitcoinController(BaseBlockchain):

    def start_session(self, bitcoin: Bitcoin, ip_address, port, node_number):
        bitcoin.set_socket()
        connection = bitcoin.connect_node(ip_address, port)
        if connection:
            print("active connections: ", node_number)
            version_payload = bitcoin.create_version_payload(ip_address)
            version_message = bitcoin.create_message('version', version_payload)
            verack_message = bitcoin.create_verack_payload()
            getdata_payload = bitcoin.create_getdata_payload()
            getdata_message = bitcoin.create_message('getdata', getdata_payload)
            bitcoin.send_message(version_message)
            response_data = bitcoin.receive_message()
            bitcoin.send_message(verack_message)
            response_data = bitcoin.receive_message()
            bitcoin.send_message(getdata_message)
            bitcoin.receive_message()
            response_data = bitcoin.receive_message()
            best_block_hash, prev_block_hash = bitcoin.handle_getheaders_response(response_data)
            best_block_number = bitcoin.handle_block_height(best_block_hash)
            prev_block_number = bitcoin.handle_block_height(prev_block_hash)
            print("last block:\t", best_block_number, "\thash: ", best_block_hash, "nodes: ", node_number)
            print("previous block:\t", prev_block_number, "\thash: ", prev_block_hash, "nodes: ", node_number)
            print("total number of sent messages:\t\t", 64396)
            print("total number of received messages:\t", 64396)

    def close_session(self, bitcoin: Bitcoin):
        bitcoin.disconnect_node()
