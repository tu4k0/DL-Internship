import os
import time

from application.btc_blockchain.btc_blockchain import BtcBlockchain
from application.eth_blockchain.eth_blockchain import EthBlockchain
from application.statistic.statistic import Statistic
from application.multithreading.thread import Thread


class CLI:
    session_status: bool
    BTC: BtcBlockchain
    ETH: EthBlockchain
    node: str

#     def __get_response_by_command(self, blockchain, message_command: str, request):
#         blockchain.send_message(request)
#         response = blockchain.receive_message()
#         return blockchain.print_response(message_command, request, response)
