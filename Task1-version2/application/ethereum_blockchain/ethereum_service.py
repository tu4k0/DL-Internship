import csv
import sys
import time

from application.database.database import Database
from application.ethereum_blockchain.ethereum_config import NODES_LIST_CSV
from application.ethereum_blockchain.ethereum import Ethereum
from application.ethereum_blockchain.ethereum_node import EthereumNode
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

    def get_nodes_from_csv(self, ip, port) -> dict[str, int]:
        found_peers = dict()
        found_peers.update({ip: port})
        search_index = 0
        with open(NODES_LIST_CSV, 'r') as nodes:
            nodes = csv.reader(nodes)
            for node_info in nodes:
                if search_index == self.node_number+1:
                    break
                else:
                    if search_index == 0:
                        search_index += 1
                    else:
                        found_peers.update({node_info[2]: 8545})
                        search_index += 1

        return found_peers

    def start_session(self):
        ethereum_light_node = EthereumNode()
        ethereum_light_node.connect()
        listening_payload = self.ethereum_p2p.create_ping_payload()
        listening_message = self.ethereum_p2p.create_message(listening_payload)
        node = self.ethereum_p2p.set_socket()
        connection = self.ethereum_p2p.connect(node, self.ip, self.port)
        if not connection:
            sys.exit('Unable to create socket')
        self.ethereum_p2p.send_message(node, listening_message)
        ping_response = self.ethereum_p2p.receive_message(node)
        if not ping_response:
            sys.exit('Node not responding')
        ethereum_light_node.send(ping_response)
        found_peers = self.get_nodes_from_csv(self.ip, self.port)
        for ip, port in found_peers.items():
            if not Database.node.find_one({'ip_address': ip, 'port': port}):
                Database.insert_node('ethereum', ip, port, False)
        while 1:
            start_time = time.perf_counter()
            node_threads = []
            for ip, port in found_peers.items():
                node = EthereumNodeThread(ip, port, self.ethereum, self.ethereum_p2p, ethereum_light_node)
                node.start()
                node_threads.append(node)
            for node in node_threads:
                node.stop()
            ethereum_statistic = EthereumStatistic(self.ethereum, self.ethereum_p2p)
            ethereum_statistic.set_amount_sent_messages()
            ethereum_statistic.set_amount_received_messages()
            ethereum_statistic.print_blockchain_info()
            avg_processing_time = time.perf_counter() - start_time
            if avg_processing_time > 5:
                time.sleep(5)
            time.sleep(5 - avg_processing_time)
            ethereum_statistic.clean_statistics()
            ethereum_statistic.clear_statistic()
