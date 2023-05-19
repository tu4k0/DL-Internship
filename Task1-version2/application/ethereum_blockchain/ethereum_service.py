import csv
import json
import sys
import time

from application.database.database import Database
from application.ethereum_blockchain.ethereum_config import ETHEREUM_PORT, ETHEREUM_MAINNET_NETWORK_ID, POLYGON_MAINNET_NETWORK_ID, BSC_MAINNET_NETWORK_ID, ETHEREUM_NODES_LIST, POLYGON_NODES_LIST, BSC_NODES_LIST
from application.ethereum_blockchain.ethereum import Ethereum
from application.ethereum_blockchain.ethereum_node import EthereumNode
from application.ethereum_blockchain.ethereum_node_thread import EthereumNodeThread
from application.ethereum_blockchain.ethereum_p2p import EthereumP2P
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

    def find_neighbours_nodes(self) -> dict[str, int]:
        found_peers = dict()
        found_peers.update({self.ip: self.port})
        search_index = 0
        with open(self.ethereum.nodes_list, 'r') as nodes:
            nodes = csv.reader(nodes)
            for node_info in nodes:
                if search_index == self.node_number + 1:
                    break
                else:
                    if search_index == 0:
                        search_index += 1
                    else:
                        ip_address = node_info[2]
                        port = int(node_info[3])
                        found_peers.update({ip_address: port})
                        search_index += 1
        for ip, port in found_peers.items():
            if not Database.node.find_one({'ip_address': ip, 'port': port}):
                Database.insert_node(self.ethereum.blockchain_type, ip, port, False)

        return found_peers

    def get_network_id(self, response) -> int:
        response = response.decode('utf-8')
        if not response:
            network_id = None
        else:
            body_start = response.find('{')
            body_end = response.rfind('}')
            network_id = int(json.loads(response[body_start:body_end + 1])['result'])

        return network_id

    def handle_ethereum_network(self, network_id):
        if network_id == ETHEREUM_MAINNET_NETWORK_ID:
            self.ethereum.network_id = ETHEREUM_MAINNET_NETWORK_ID
            self.ethereum.blockchain_type = 'ethereum'
            self.ethereum.nodes_list = ETHEREUM_NODES_LIST
        elif network_id == POLYGON_MAINNET_NETWORK_ID:
            self.ethereum.network_id = POLYGON_MAINNET_NETWORK_ID
            self.ethereum.blockchain_type = 'polygon'
            self.ethereum.nodes_list = POLYGON_NODES_LIST
        elif network_id == BSC_MAINNET_NETWORK_ID:
            self.ethereum.network_id = BSC_MAINNET_NETWORK_ID
            self.ethereum.blockchain_type = 'bsc'
            self.ethereum.nodes_list = BSC_NODES_LIST

        return self

    def start_session(self):
        ethereum_light_node = EthereumNode()
        ethereum_light_node.connect()
        version_payload = self.ethereum_p2p.create_version_payload()
        version_message = self.ethereum_p2p.create_message(version_payload)
        node = self.ethereum_p2p.set_socket()
        connection = self.ethereum_p2p.connect(node, self.ip, self.port)
        if not connection:
            sys.exit('Unable to create connection with node')
        self.ethereum_p2p.send_message(node, version_message)
        version_response = self.ethereum_p2p.receive_message(node)
        if not version_response:
            sys.exit('Node not responding')
        ethereum_light_node.send(version_response)
        network_id = self.get_network_id(version_response)
        self.handle_ethereum_network(network_id)
        found_peers = self.find_neighbours_nodes()
        while 1:
            start_time = time.perf_counter()
            node_threads = []
            for ip in found_peers:
                node = EthereumNodeThread(ip, ETHEREUM_PORT, self.ethereum, self.ethereum_p2p, ethereum_light_node)
                node.start()
                node_threads.append(node)
            for node in node_threads:
                node.stop()
            ethereum_statistic = EthereumStatistic(self.ethereum, self.ethereum_p2p)
            ethereum_statistic.collect_blockchain_info()
            ethereum_statistic.print_statistic()
            avg_processing_time = time.perf_counter() - start_time
            if avg_processing_time > 5:
                time.sleep(5)
            time.sleep(5 - avg_processing_time)
            ethereum_statistic.clean_statistics()
            ethereum_statistic.clear_statistic()
