import sys

from application.bitcoin_blockchain.bitcoin_controller import BitcoinController
from application.ethereum_blockchain.ethereum_controller import EthereumController
from application.bitcoin_blockchain.bitcoin_config import *
from application.ethereum_blockchain.ethereum_config import *


class CLI:
    cli_arguments: list

    def __init__(self):
        self.cli_arguments = sys.argv

    def run(self):
        node = self.cli_arguments[1].split(':')
        ip_address = node[0]
        port = int(node[1])
        node_number = int(self.cli_arguments[2])
        user_request = [ip_address, port, node_number]
        if port == BITCOIN_MAINNET_PORT:
            bitcoin_controller = BitcoinController(user_request)
            bitcoin_controller.start_data_collecting_session()
        elif port == ETHEREUM_MAINNET_PORT:
            ethereum_controller = EthereumController(user_request)
            ethereum_controller.start_data_collecting_session()
        else:
            raise Exception("Invalid port")
