from application.ethereum_blockchain.ethereum_service import EthereumService


class EthereumController:
    user_request: list
    ethereum_service: EthereumService

    def __init__(self, user_request):
        self.user_request = user_request
        self.ethereum_service = EthereumService(user_request)

    def start_data_collecting_session(self):
        self.ethereum_service.start_session()

