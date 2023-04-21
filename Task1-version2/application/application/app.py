import binascii
import os
import time
import sys

from application.bitcoin_blockchain.bitcoin_controller import BitcoinController
from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P
from application.bitcoin_blockchain.bitcoin_config import *
from application.eth_blockchain.eth_blockchain import EthBlockchain
from application.eth_blockchain.eth_config import *


class CLI:
    BTC: BitcoinP2P
    ETH: EthBlockchain
    cli_arguments: list

    def __init__(self, bitcoin: BitcoinP2P):
        self.cli_arguments = sys.argv
        self.bitcoin = bitcoin

    def run(self):
        node = self.cli_arguments[1].split(':')
        ip_address = node[0]
        port = int(node[1])
        node_number = int(self.cli_arguments[2])
        if port == btc_mainnet_port:
            bitcoin_controller = BitcoinController(self.bitcoin)
            bitcoin_controller.start_session(ip_address=ip_address, port=port, node_number=node_number)
        elif port == eth_mainnet_port:
            print("Ethereum")
        else:
            raise Exception("Invalid port")


#     def __get_response_by_command(self, blockchain, message_command: str, request):
#         blockchain.send_message(request)
#         response = blockchain.receive_message()
#         return blockchain.print_response(message_command, request, response)
