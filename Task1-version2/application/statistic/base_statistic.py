import os
from abc import abstractmethod, ABC

from application.bitcoin_blockchain.bitcoin import Bitcoin
from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P
from application.ethereum_blockchain.ethereum import Ethereum
from application.ethereum_blockchain.ethereum_p2p import EthereumP2P


class BaseStatistic(ABC):
    def __init__(self, blockchain: Bitcoin | Ethereum, blockchain_p2p: BitcoinP2P | EthereumP2P):
        self.blockchain = blockchain
        self.blockchain_p2p = blockchain_p2p
        self.active_connections = 0
        self.best_block_number = 0
        self.best_block_hash = None
        self.nodes_1 = 0
        self.prev_block_number = None
        self.prev_block_hash = None
        self.nodes_2 = ''
        self.sent_messages = 0
        self.received_messages = 0

    @abstractmethod
    def collect_blockchain_info(self):
        pass

    @abstractmethod
    def print_statistic(self):
        pass

    @abstractmethod
    def clear_statistic(self):
        pass

    @property
    def get_amount_sent_messages(self):
        return self.blockchain_p2p.requests

    @property
    def get_amount_received_messages(self):
        return self.blockchain_p2p.responses

    def clean_statistics(self):
        os.system('cls')
