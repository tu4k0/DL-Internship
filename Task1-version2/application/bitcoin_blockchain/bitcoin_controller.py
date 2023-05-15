from application.bitcoin_blockchain.bitcoin_service import BitcoinService
from application.database.database import Database


class BitcoinController:
    user_request: list
    bitcoin_service: BitcoinService
    database: Database

    def __init__(self, user_request, database):
        self.user_request = user_request
        self.bitcoin_service = BitcoinService(user_request)
        self.database = database

    def start_data_collecting_session(self):
        self.bitcoin_service.start_session(self.database)
