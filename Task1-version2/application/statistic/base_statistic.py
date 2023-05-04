import sys
from abc import abstractmethod, ABC

from application.bitcoin_blockchain.bitcoin import Bitcoin
from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P
from application.ethereum_blockchain.ethereum import Ethereum
from application.ethereum_blockchain.ethereum_p2p import EthereumP2P


class BaseStatistic(ABC):
    def __init__(self, blockchain: Bitcoin | Ethereum, blockchain_p2p: BitcoinP2P | EthereumP2P):
        self.blockchain = blockchain
        self.blockchain_p2p = blockchain_p2p

    @abstractmethod
    def print_blockchain_info(self):
        pass

    @abstractmethod
    def clear_statistic(self):
        pass

    def set_amount_sent_messages(self):
        self.blockchain.amount_sent_messages = self.blockchain_p2p.requests

    def set_amount_received_messages(self):
        self.blockchain.amount_received_messages = self.blockchain_p2p.responses

    @property
    def get_amount_sent_messages(self):
        return self.blockchain.amount_sent_messages

    @property
    def get_amount_received_messages(self):
        return self.blockchain.amount_received_messages

    def clean_statistics(self, statistic_rows):
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE = '\x1b[2K'
        for _ in range(statistic_rows):
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)
