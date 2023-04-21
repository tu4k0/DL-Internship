from application.bitcoin_blockchain.bitcoin_service import BitcoinService


class BitcoinController:
    user_request: list
    bitcoin_service: BitcoinService

    def __init__(self, user_request):
        self.user_request = user_request
        self.bitcoin_service = BitcoinService(user_request)

    def start_data_collecting_session(self):
        self.bitcoin_service.start_session(self.user_request)
        self.print_blockchain_info()

    def print_blockchain_info(self):
        print("last block:\t", self.bitcoin_service.bitcoin.best_block_height, "\thash: ", self.bitcoin_service.bitcoin.best_block_hash, "nodes: ", self.bitcoin_service.bitcoin.node_number)
        print("previous block:\t", self.bitcoin_service.bitcoin.previous_block_height, "\thash: ",  self.bitcoin_service.bitcoin.previous_block_hash, "nodes: ", self.bitcoin_service.bitcoin.node_number)
        print("total number of sent messages:\t\t",  self.bitcoin_service.bitcoin.amount_sent_messages)
        print("total number of received messages:\t",  self.bitcoin_service.bitcoin.amount_received_messages)

