from application.btc_blockchain.btc_blockchain import BtcBlockchain

import threading

from application.btc_blockchain.btc_blockchain import BtcBlockchain


class Statistic:
    requests: int
    responses: list
    connections: list
    threads: list
    btc_blockchains_objects: list
    nodes: dict
    etc_blockchain_objects: list

    def __init__(self):
        self.requests = 0
        self.responses = []
        self.connections = []
        self.threads = []
        self.nodes = {}
        self.btc_blockchains_objects = []

    def show_blockchain_statistic(self):
        for object in self.btc_blockchains_objects:
            print(object.requests)

    def print_nodes(self):
        print('Nodes: ')
        if self.nodes:
            node_counter = 1
            for key, value in self.nodes.items():
                print('Node', node_counter, '  ', f'{key},', value)
                node_counter += 1
        else:
            print('Failed to get node peers! Try again')

