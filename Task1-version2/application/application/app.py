import binascii
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
        ip_address = node[0]
        port = int(node[1])
        node_number = int(self.cli_arguments[2])
        if port == btc_mainnet_port:
            start_time = time.time()
            CLI.BTC = BtcBlockchain()
            CLI.BTC.set_socket()
            connection = CLI.BTC.connect_node(ip_address, port)
            if connection:
                # Create Messages
                version_payload = CLI.BTC.create_version_payload(ip_address)
                version_message = CLI.BTC.create_message('version', version_payload)
                verack_message = CLI.BTC.create_verack_payload()
                getdata_payload = CLI.BTC.create_getdata_payload()
                getdata_message = CLI.BTC.create_message('getdata', getdata_payload)

                # Send message "version"
                CLI.BTC.send_message(version_message)
                response_data = CLI.BTC.receive_message()

                # Send message "verack"
                CLI.BTC.send_message(verack_message)
                response_data = CLI.BTC.receive_message()

                # Send message "getdata"
                CLI.BTC.send_message(getdata_message)
                CLI.BTC.receive_message()
                response_data = CLI.BTC.receive_message()
                result = str(response_data)

                index = result.find("getheaders")
                if index == -1:
                    getheaders = CLI.BTC.receive_message()
                    res = str(getheaders)
                    index = res.find("getheaders")
                    Block_hash = binascii.hexlify(getheaders)[index + 40:index + 104]
                    hash = Block_hash.decode("utf-8")
                    response = bytearray.fromhex(hash)
                    response.reverse()
                    print('Bitcoin best block hash: ', response.hex())
                else:
                    Block_hash = binascii.hexlify((response_data))[140:204]
                    hash = Block_hash.decode("utf-8")
                    response = bytearray.fromhex(hash)
                    response.reverse()
                    print('Bitcoin best block hash: ', response.hex())

                print('Retreiving block hash data execution time: ', time.time() - start_time)

                # Disconnect from node and Close the TCP connection
                CLI.BTC.disconnect_node()
        elif port == eth_mainnet_port:
            print("Ethereum")
        else:
            raise Exception("Invalid port")


#     def __get_response_by_command(self, blockchain, message_command: str, request):
#         blockchain.send_message(request)
#         response = blockchain.receive_message()
#         return blockchain.print_response(message_command, request, response)
