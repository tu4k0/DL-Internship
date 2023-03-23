import threading

from application.multithreading.node_thread import NodeThread
from application.btc_blockchain.btc_blockchain import BtcBlockchain


class Thread():
    node_thread: NodeThread

    def __init__(self):
        self.node_thread = NodeThread()

    def set_threads(self, nodes, blockchain, statistic):
        delete_nodes = []
        for key, value in nodes.items():
            try:
                node = threading.Thread(target=self.node_thread.collect_blockchain_info, daemon=True, args=(
                    blockchain,
                    key,
                    value,
                    statistic
                ))
                node.start()
                node.join()
            except TimeoutError:
                delete_nodes.append(key)
        for node in delete_nodes:
            nodes.pop(node, None)
