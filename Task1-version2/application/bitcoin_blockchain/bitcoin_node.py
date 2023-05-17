from application.base_blockchain.base_node import BaseNode
from application.bitcoin_blockchain.bitcoin_config import BITCOIN_MAINNET_PORT


class BitcoinNode(BaseNode):

    def __init__(self):
        super().__init__()
        self.ip = '127.0.0.1'
        self.port = BITCOIN_MAINNET_PORT

    def set_node(self):
        self.node.bind((self.ip, self.port))

    def present_messages(self, data):
        print(f'{data}\n')
