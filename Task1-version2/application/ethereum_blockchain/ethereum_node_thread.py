import json

from application.database.database import Database
from application.ethereum_blockchain.ethereum import Ethereum
from application.ethereum_blockchain.ethereum_node import EthereumNode
from application.ethereum_blockchain.ethereum_p2p import EthereumP2P
from application.multithreading.base_thread import BaseThread


class EthereumNodeThread(BaseThread):
    ip: str
    port: int
    ethereum: Ethereum
    ethereum_p2p: EthereumP2P
    ethereum_light_node: EthereumNode

    def __init__(self, ip, port, ethereum: Ethereum, ethereum_p2p: EthereumP2P, ethereum_light_node: EthereumNode):
        super().__init__()
        self.ip = ip
        self.port = port
        self.ethereum = ethereum
        self.ethereum_p2p = ethereum_p2p
        self.ethereum_light_node = ethereum_light_node

    def run(self):
        best_block_hash, best_block_number, prev_block_number, prev_block_hash = None, None, None, None
        listening_payload = self.ethereum_p2p.create_ping_payload()
        listening_message = self.ethereum_p2p.create_message(listening_payload)
        node = self.ethereum_p2p.set_socket()
        connection = self.ethereum_p2p.connect(node, self.ip, self.port)
        if connection:
            self.ethereum_p2p.send_message(node, listening_message)
            ping_response = self.ethereum_p2p.receive_message(node)
            status = self.handle_node_listening_status(ping_response)
            if status:
                Database.update_node_status(self.ip, self.ethereum.blockchain_type, True)
                self.ethereum_light_node.send(ping_response)
                self.ethereum.active_connections += 1
                best_block_number_payload = self.ethereum_p2p.create_best_block_height_payload()
                best_block_number_message = self.ethereum_p2p.create_message(best_block_number_payload)
                self.ethereum_p2p.send_message(node, best_block_number_message)
                best_block_number_response = self.ethereum_p2p.receive_message(node)
                self.ethereum_light_node.send(best_block_number_response)
                best_block_number = self.get_best_block_number(best_block_number_response)
                if isinstance(best_block_number, int):
                    best_block_hash_payload = self.ethereum_p2p.create_getblock_by_number_payload(best_block_number)
                    best_block_hash_message = self.ethereum_p2p.create_message(best_block_hash_payload)
                    self.ethereum_p2p.send_message(node, best_block_hash_message)
                    best_block_hash_response = self.ethereum_p2p.receive_message(node)
                    self.ethereum_light_node.send(best_block_hash_response)
                    best_block_hash = self.get_best_block_hash(best_block_hash_response)
                    prev_block_number = best_block_number - 1
                    prev_block_hash = self.get_previous_block_hash(best_block_hash_response)
        self.ethereum.best_block_hashes.append(best_block_hash)
        self.ethereum.best_block_numbers.append(best_block_number)
        self.ethereum.prev_block_hashes.append(prev_block_hash)
        self.ethereum.prev_block_numbers.append(prev_block_number)
        node.close()

    def handle_node_listening_status(self, response):
        status = str
        if len(response) != 0:
            response = str(response)
            result_index = response.find("result")
            if result_index != -1:
                result = response[result_index + 8:]
                status = bool(result[:result.find("}")])
            return status
        else:
            status = False

        return status

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

    def get_best_block_hash(self, response) -> any:
        if response:
            best_block_hash = self.decode_response_message(response)['result']['hash']
        else:
            best_block_hash = None

        return best_block_hash

    def get_best_block_number(self, response):
        if response:
            best_block_number = self.decode_response_message(response)['result']
            best_block_number = int(best_block_number, 16)
        else:
            best_block_number = None

        return best_block_number

    def get_previous_block_hash(self, response):
        if response:
            previous_block_hash = self.decode_response_message(response)['result']['parentHash']
        else:
            previous_block_hash = None

        return previous_block_hash
