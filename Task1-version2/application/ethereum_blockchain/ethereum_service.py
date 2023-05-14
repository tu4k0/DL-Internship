import csv
import time

from application.ethereum_blockchain.ethereum_config import NODES_LIST_CSV
from application.ethereum_blockchain.ethereum import Ethereum
from application.ethereum_blockchain.ethereum_p2p import EthereumP2P
from application.ethereum_blockchain.ethereum_node_thread import EthereumNodeThread
from application.ethereum_blockchain.ethereum_statistic import EthereumStatistic


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

    def get_nodes_from_csv(self) -> dict[str, int]:
        found_peers = dict()
        found_peers.update({self.ip: self.port})
        search_index = 0
        with open(NODES_LIST_CSV, 'r') as nodes:
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
        nodes = self.get_nodes_from_csv()
        while True:
            for ip, port in nodes.items():
                node = EthereumNodeThread(ip, port, self.ethereum, self.ethereum_p2p)
                node.start()
                node_threads.append(node)
            for node in node_threads:
                node.stop()
            ethereum_statistic = EthereumStatistic(self.ethereum, self.ethereum_p2p)
            ethereum_statistic.set_amount_sent_messages()
            ethereum_statistic.set_amount_received_messages()
            ethereum_statistic.print_blockchain_info()
            time.sleep(5)
            ethereum_statistic.clean_statistics()
            ethereum_statistic.clear_statistic()
