import sys

from application.bitcoin_blockchain.bitcoin_controller import BitcoinController
from application.bitcoin_blockchain.bitcoin_config import *
from application.ethereum_blockchain.eth_config import *


class CLI:
    cli_arguments: list

    def __init__(self):
        self.cli_arguments = sys.argv

    def run(self):
        node = self.cli_arguments[1].split(':')
        ip_address = node[0]
        port = int(node[1])
        node_number = int(self.cli_arguments[2])
        if port == btc_mainnet_port:
            user_request = [ip_address, port, node_number]
            bitcoin_controller = BitcoinController(user_request)
            bitcoin_controller.start_data_collecting_session()
        elif port == eth_mainnet_port:
            print("Ethereum")
        else:
            raise Exception("Invalid port")
