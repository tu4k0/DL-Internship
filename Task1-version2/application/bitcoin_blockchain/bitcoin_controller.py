from application.bitcoin_blockchain.bitcoin_service import BitcoinService


class BitcoinController:
    user_request: list
    bitcoin_service: BitcoinService

    def __init__(self, user_request):
        self.user_request = user_request
        self.bitcoin_service = BitcoinService(user_request)

    def start_data_collecting_session(self):
        self.bitcoin_service.start_session(self.user_request)
