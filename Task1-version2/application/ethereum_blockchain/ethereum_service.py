import csv
import json
import sys
import time

from application.ethereum_blockchain.ethereum import Ethereum
from application.ethereum_blockchain.ethereum_p2p import EthereumP2P
from application.ethereum_blockchain.ethereum_node_thread import EthereumNodeThread

nodes_list = 'C:/Users/Admin/Desktop/Tu4k0/DL-Internship/Task1-version2/application/ethereum_blockchain/ethereum-nodestrackerlist.csv'


class EthereumService:
    ip: str
    port: int
    node_number: int
    ethereum: Ethereum
    ethereum_p2p: EthereumP2P

    def __init__(self, user_request):
        self.ethereum = Ethereum()
        self.ethereum_p2p = EthereumP2P()
        self.ip = user_request[0]
        self.port = user_request[1]
        self.node_number = user_request[2]

    def get_nodes(self):
        found_peers = dict()
        found_peers.update({self.ip: self.port})
        search_index = 0
        with open(nodes_list, 'r') as nodes:
            nodes = csv.reader(nodes)
            for node_info in nodes:
                if search_index == self.node_number:
                    break
                else:
                    if search_index == 0:
                        search_index += 1
                    else:
                        found_peers.update({node_info[2]: 8545})
                        search_index += 1

        return found_peers

    def start_session(self):
        node_threads = []
        nodes = self.get_nodes()
        while True:
            start_time = time.time()
            for ip, port in nodes.items():
                node = EthereumNodeThread(ip, port, self.ethereum, self.ethereum_p2p)
                node.start()
                node_threads.append(node)
            for node in node_threads:
                node.join()
            self.ethereum.amount_sent_messages = self.ethereum_p2p.requests
            self.ethereum.amount_received_messages = self.ethereum_p2p.responses
            self.print_blockchain_info()
            self.clear_statistic()

    def print_blockchain_info(self):
        last_block_number = None
        last_block_hash = None
        prev_block_height = None
        prev_block_hash = None
        print("active connections:\t", self.ethereum.active_connections)
        for bbn in self.ethereum.best_block_numbers:
            if bbn is not None:
                last_block_number = bbn
        for bbh in self.ethereum.best_block_hashes:
            if bbh is not None:
                last_block_hash = bbh
        print("last block:\t", last_block_number, "\thash: ",
              last_block_hash, "nodes: ", self.ethereum.best_block_hashes.count(last_block_hash))
        for pbn in self.ethereum.prev_block_numbers:
            if pbn is not None:
                prev_block_height = pbn
        for pbh in self.ethereum.prev_block_hashes:
            if pbh is not None:
                prev_block_hash = pbh
        print("previous block:\t", prev_block_height, "\thash: ",
              prev_block_hash, "nodes: ",
              self.ethereum.prev_block_hashes.count(prev_block_hash))
        print("total number of sent messages:\t\t", self.ethereum.amount_sent_messages)
        print("total number of received messages:\t", self.ethereum.amount_received_messages)

    def clear_statistic(self):
        self.ethereum.best_block_numbers.clear()
        self.ethereum.best_block_hashes.clear()
        self.ethereum.prev_block_numbers.clear()
        self.ethereum.prev_block_hashes.clear()
        self.ethereum.active_connections = 0

    def close_session(self):
        sys.exit('0')
