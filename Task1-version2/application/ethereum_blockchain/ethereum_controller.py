from application.ethereum_blockchain.ethereum_service import EthereumService


class EthereumController:
    user_request: list
    ethereum_service: EthereumService

    def __init__(self, user_request):
        self.user_request = user_request
        self.ethereum_service = EthereumService(user_request)

    def start_data_collecting_session(self):
        self.ethereum_service.start_session(self.user_request)
        self.print_blockchain_info()

    def print_blockchain_info(self):
        print("last block:\t", self.ethereum_service.ethereum.best_block_height, "\thash: ", self.ethereum_service.ethereum.best_block_hash, "nodes: ", self.ethereum_service.ethereum.node_number)
        print("previous block:\t", self.ethereum_service.ethereum.previous_block_height, "\thash: ",  self.ethereum_service.ethereum.previous_block_hash, "nodes: ", self.ethereum_service.ethereum.node_number)
        print("total number of sent messages:\t\t",  self.ethereum_service.ethereum.amount_sent_messages)
        print("total number of received messages:\t",  self.ethereum_service.ethereum.amount_received_messages)

