from application.base_blockchain.base_node import BaseNode
from application.ethereum_blockchain.ethereum_config import ETHEREUM_MAINNET_PORT


class EthereumNode(BaseNode):

    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.port = ETHEREUM_MAINNET_PORT

    def set_node(self):
        self.node.bind((self.ip, self.port))

    def print_messages(self, data):
        print(data)
