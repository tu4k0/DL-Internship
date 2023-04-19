import os
import time
import sys

from application.btc_blockchain.btc_blockchain import BtcBlockchain
from application.btc_blockchain.btc_config import *
from application.eth_blockchain.eth_blockchain import EthBlockchain
from application.eth_blockchain.eth_config import *
from application.statistic.statistic import Statistic
from application.multithreading.thread import Thread


class CLI:
    BTC: BtcBlockchain
    ETH: EthBlockchain
    cli_arguments: list

    def __init__(self):
        self.cli_arguments = sys.argv

    def run(self):
        node = self.cli_arguments[1].split(':')
        ip = node[0]
        port = int(node[1])
        node_number = int(self.cli_arguments[2])
        if port == btc_mainnet_port:
            print("BTC")
        elif port == eth_mainnet_port:
            print("Ethereum")
        else:
            raise Exception("Invalid port")




#     def __get_response_by_command(self, blockchain, message_command: str, request):
#         blockchain.send_message(request)
#         response = blockchain.receive_message()
#         return blockchain.print_response(message_command, request, response)
