from application.base_blockchain.base_node import BaseNode
from application.ethereum_blockchain.ethereum_config import ETHEREUM_PORT


class EthereumNode(BaseNode):

    def __init__(self):
        super().__init__()
        self.ip = '127.0.0.1'
        self.port = ETHEREUM_PORT

    def set_node(self):
        self.node.bind((self.ip, self.port))

    def present_messages(self, data):
        print(f'{data}\n')
