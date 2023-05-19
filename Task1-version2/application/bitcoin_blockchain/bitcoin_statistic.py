import time

from application.database.database import Database
from application.bitcoin_blockchain.bitcoin import Bitcoin
from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P
from application.statistic.base_statistic import BaseStatistic


class BitcoinStatistic(BaseStatistic):
    def __init__(self, bitcoin: Bitcoin, bitcoin_p2p: BitcoinP2P):
        super().__init__(bitcoin, bitcoin_p2p)

    def collect_blockchain_info(self):
        for bbn in self.blockchain.best_block_numbers:
            if bbn is not None:
                if self.best_block_number < bbn:
                    self.best_block_number = bbn
        self.best_block_hash = self.blockchain.best_block_hashes[self.blockchain.best_block_numbers.index(self.best_block_number)]
        self.prev_block_number = self.blockchain.prev_block_numbers[self.blockchain.best_block_numbers.index(self.best_block_number)]
        self.prev_block_hash = self.blockchain.prev_block_hashes[self.blockchain.best_block_numbers.index(self.best_block_number)]
        self.active_connections = self.blockchain.active_connections
        self.sent_messages = self.get_amount_sent_messages
        self.received_messages = self.get_amount_received_messages
        self.nodes_1 = self.blockchain.best_block_hashes.count(self.best_block_hash)
        self.nodes_2 = self.blockchain.prev_block_hashes.count(self.prev_block_hash)
        created_at = time.strftime("%Y-%m-%d %H:%M:%S")
        Database.insert_blockchain(
            'bitcoin',
            self.active_connections,
            self.best_block_number,
            self.best_block_hash,
            self.nodes_1,
            self.prev_block_number,
            self.prev_block_hash,
            self.nodes_2,
            self.sent_messages,
            self.received_messages,
            created_at
        )

    def print_statistic(self):
        print("blockchain:\tbitcoin", )
        print("active connections:\t", self.active_connections)
        print("last block:\t", self.best_block_number, "\thash: ", self.best_block_hash, "nodes: ", self.nodes_1)
        print("previous block:\t", self.prev_block_number, "\thash: ", self.prev_block_hash, "nodes: ", self.nodes_2)
        print("total number of sent messages:\t\t", self.sent_messages)
        print("total number of received messages:\t", self.received_messages)

    def clear_statistic(self):
        self.blockchain.best_block_numbers.clear()
        self.blockchain.best_block_hashes.clear()
        self.blockchain.prev_block_numbers.clear()
        self.blockchain.prev_block_hashes.clear()
        self.blockchain.active_connections = 0
