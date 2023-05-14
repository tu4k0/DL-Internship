from application.base_blockchain.base_node import BaseNode


class BitcoinNode(BaseNode):

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port

    def set_node(self):
        self.node.bind((self.ip, self.port))

    def print_messages(self, data):
        print(data)
