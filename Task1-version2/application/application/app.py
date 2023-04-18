import os
import time
import sys

from application.btc_blockchain.btc_blockchain import BtcBlockchain
from application.eth_blockchain.eth_blockchain import EthBlockchain
from application.statistic.statistic import Statistic
from application.multithreading.thread import Thread


class CLI:
    session_status: bool
    BTC: BtcBlockchain
    ETH: EthBlockchain
    node: str
    cli_arguments: argparse.ArgumentParser

    def __init__(self):
        self.cli_arguments = argparse.ArgumentParser(description="Bitcoin/Ethereum P2P network implementation")
        self.cli_arguments.add_argument("-ip", dest="ip_address", required=True, type=str)
        self.cli_arguments.add_argument("-port", dest="port", required=True, type=int)
        self.cli_arguments.add_argument("-num", dest="node_number", default=1, type=int)

    def run(self):
        print(self.cli_arguments.parse_args())


cli = CLI()
cli.run()
#     def __get_response_by_command(self, blockchain, message_command: str, request):
#         blockchain.send_message(request)
#         response = blockchain.receive_message()
#         return blockchain.print_response(message_command, request, response)
