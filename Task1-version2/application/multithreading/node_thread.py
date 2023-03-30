import threading

from application.btc_blockchain.btc_blockchain import BtcBlockchain


class NodeThread(threading.Thread):
    threads = []
    sockets = []
    requests = []
    responses = []
    lock = threading.RLock()

    def __init__(self):
        super().__init__()

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



