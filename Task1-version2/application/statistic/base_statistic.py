from abc import abstractmethod, ABC

from application.bitcoin_blockchain.bitcoin import Bitcoin
from application.ethereum_blockchain.ethereum import Ethereum


class BaseStatistic(ABC):
    def __init__(self, blockchain: Bitcoin | Ethereum):
        self.blockchain = blockchain

    @abstractmethod
    def print_blockchain_info(self):
        pass

    @abstractmethod
    def clear_statistic(self):
        pass

    @property
    def get_amount_sent_messages(self):
        return self.blockchain.amount_sent_messages

    @property
    def get_amount_received_messages(self):
        return self.blockchain.amount_received_messages
