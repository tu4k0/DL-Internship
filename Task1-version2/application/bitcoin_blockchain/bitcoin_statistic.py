from application.bitcoin_blockchain.bitcoin import Bitcoin
from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P
from application.database.database import Database
from application.statistic.base_statistic import BaseStatistic


class BitcoinStatistic(BaseStatistic):
    def __init__(self, bitcoin: Bitcoin, bitcoin_p2p: BitcoinP2P):
        super().__init__(bitcoin, bitcoin_p2p)

    def print_blockchain_info(self, database: Database):
        last_block_number = None
        last_block_hash = None
        prev_block_height = None
        prev_block_hash = None
        print("active connections:\t", self.blockchain.active_connections)
        for bbn in self.blockchain.best_block_numbers:
            if bbn is not None:
                last_block_number = bbn
                break
        for bbh in self.blockchain.best_block_hashes:
            if bbh is not None:
                last_block_hash = bbh
                break
        nodes_1 = self.blockchain.best_block_hashes.count(last_block_hash)
        print("last block:\t", last_block_number, "\thash: ", last_block_hash, "nodes: ", nodes_1)
        for pbn in self.blockchain.prev_block_numbers:
            if pbn is not None:
                prev_block_height = pbn
                break
        for pbh in self.blockchain.prev_block_hashes:
            if pbh is not None:
                prev_block_hash = pbh
                break
        nodes_2 = self.blockchain.prev_block_hashes.count(prev_block_hash)
        print("previous block:\t", prev_block_height, "\thash: ", prev_block_hash, "nodes: ", nodes_2)
        print("total number of sent messages:\t\t", self.get_amount_sent_messages)
        print("total number of received messages:\t", self.get_amount_received_messages)
        database.insert_blockchain('bitcoin', self.blockchain.active_connections, last_block_number, last_block_hash, nodes_1, prev_block_height, prev_block_hash, nodes_2, self.get_amount_sent_messages, self.get_amount_received_messages)

    def clear_statistic(self):
        self.blockchain.best_block_numbers.clear()
        self.blockchain.best_block_hashes.clear()
        self.blockchain.prev_block_numbers.clear()
        self.blockchain.prev_block_hashes.clear()
        self.blockchain.active_connections = 0
