import json

from application.ethereum_blockchain.ethereum import Ethereum
from application.ethereum_blockchain.ethereum_p2p import EthereumP2P


class EthereumService:
    ethereum: Ethereum
    ethereum_p2p: EthereumP2P

    def __init__(self, user_request):
        self.ethereum = Ethereum(ip_address=user_request[0], port=user_request[1], node_number=user_request[2])
        self.ethereum_p2p = EthereumP2P()

    def start_session(self, user_request):
        ip_address = user_request[0]
        port = user_request[1]
        node_number = user_request[2]
        self.ethereum_p2p.set_socket()
        connection = self.ethereum_p2p.connect_node(ip_address, port)
        if connection:
            print("active connections: ", node_number)
            best_block_payload = self.ethereum_p2p.create_best_block_height_payload()
            best_block_message = self.ethereum_p2p.make_message(best_block_payload)
            self.ethereum_p2p.send_message(best_block_message)
            best_block_response = self.ethereum_p2p.receive_message()
            best_block_number = int(self.decode_response_message(best_block_response)['result'], 16)
            best_block_hash_payload = self.ethereum_p2p.create_getblock_by_number_payload(best_block_number)
            best_block_hash_message = self.ethereum_p2p.make_message(best_block_hash_payload)
            self.ethereum_p2p.send_message(best_block_hash_message)
            best_block_response = self.ethereum_p2p.receive_message()
            best_block_hash = self.decode_response_message(best_block_response)['result']['hash']
            prev_block_number = best_block_number - 1
            prev_block_hash_payload = self.ethereum_p2p.create_getblock_by_number_payload(prev_block_number)
            prev_block_hash_message = self.ethereum_p2p.make_message(prev_block_hash_payload)
            self.ethereum_p2p.send_message(prev_block_hash_message)
            prev_block_hash_response = self.ethereum_p2p.receive_message()
            prev_block_hash = best_block_hash
            self.ethereum.best_block_height = best_block_number
            self.ethereum.best_block_hash = best_block_hash
            self.ethereum.previous_block_height = prev_block_number
            self.ethereum.previous_block_hash = prev_block_hash
            self.ethereum.amount_sent_messages = self.ethereum_p2p.requests
            self.ethereum.amount_received_messages = self.ethereum_p2p.responses

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

    def close_session(self):
        self.ethereum_p2p.disconnect_node()
