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
            best_block_number_payload = self.ethereum_p2p.create_best_block_height_payload()
            best_block_number_message = self.ethereum_p2p.make_message(best_block_number_payload)
            self.ethereum_p2p.send_message(best_block_number_message)
            best_block_number_response = self.ethereum_p2p.receive_message()
            best_block_number = self.get_best_block_number(best_block_number_response)
            best_block_hash_payload = self.ethereum_p2p.create_getblock_by_number_payload(best_block_number)
            best_block_hash_message = self.ethereum_p2p.make_message(best_block_hash_payload)
            self.ethereum_p2p.send_message(best_block_hash_message)
            best_block_response = self.ethereum_p2p.receive_message()
            self.ethereum.best_block_height = best_block_number
            self.ethereum.best_block_hash = self.get_best_block_hash(best_block_response)
            self.ethereum.previous_block_height = best_block_number - 1
            self.ethereum.previous_block_hash = self.get_previous_block_hash(best_block_response)
            self.ethereum.amount_sent_messages = self.ethereum_p2p.requests
            self.ethereum.amount_received_messages = self.ethereum_p2p.responses

    def decode_response_message(self, response):
        message = {}
        response = response.decode('utf-8')
        if not response:
            message.update(result=None)
        else:
            status = message['status'] = response[9:15]
            type = message['type'] = response[43:47]
            length = message.update(length=len(response))
            body_start = response.find('{')
            if 'transactions' in response:
                body_end = response.rfind('transactions')
                response = response[body_start:body_end - 2] + '}' + '}'
                message.update(result=json.loads(response)['result'])
            else:
                if response.rfind('parentHash') != -1:
                    body_end = response.rfind('parentHash') + 80
                    response = response[body_start:body_end] + '}' + '}'
                    message.update(result=json.loads(response)['result'])
                else:
                    body_end = response.rfind('}')
                    message.update(result=json.loads(response[body_start:body_end + 1])['result'])

            return message

    def get_best_block_hash(self, response):
        best_block_hash = self.decode_response_message(response)['result']['hash']

        return best_block_hash

    def get_best_block_number(self, response):
        best_block_number = self.decode_response_message(response)['result']
        best_block_number = int(best_block_number, 16)

        return best_block_number

    def get_previous_block_hash(self, response):
        previous_block_hash = self.decode_response_message(response)['result']['parentHash']

        return previous_block_hash

    def close_session(self):
        self.ethereum_p2p.disconnect_node()
