import threading
import time

from application.btc_blockchain.btc_blockchain import BtcBlockchain
from application.statistic.statistic import Statistic
from application.btc_blockchain.btc_config import *
from application.base_blockchain.base_blockchain import BaseBlockchain


class NodeThread(threading.Thread):
    threads = []
    sockets = []
    requests = []
    responses = []
    lock = threading.Lock()

    def __init__(self):
        super().__init__()

    # def set_thread(self, nodes, blockchain):
    #     for key, value in nodes.items():
    #         blockchain.set_socket()
    #         connection = blockchain.connect_node(ip_address=key, port=value)
    #         thread = threading.Thread(target=self.collect_blockchain_info, args=(blockchain, key,))
    #         thread.start()
    #         print('\nNode: ', f'{key}:{value}')
    #         self.threads.append(thread)
    #         thread.join()

    def set_node_socket(self, blockchain, ip_address, port):
        if type(blockchain) == BtcBlockchain:
            node_socket = BtcBlockchain()
            node_socket.set_socket()
            node_socket.connect_node(ip_address, port)
            return node_socket

    def collect_blockchain_info(self, blockchain, ip_address, port, statistic):
        with self.lock:
            node = self.set_node_socket(blockchain, ip_address, port)
            node.execute_message(command_name='version', payload=ip_address)
            node.execute_message(command_name='verack')
            node.execute_message(command_name='getheaders')
            node.execute_message(command_name='ping')
            statistic.connections.append(node.socket)
            statistic.btc_blockchains_objects.append(node)



