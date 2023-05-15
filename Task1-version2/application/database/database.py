import pymongo

from typing import Mapping, Any
from pymongo import MongoClient

from application.database.node_model import NodeModel
from application.database.blockchain_model import BlockchainModel


class Database():
    db_instance: MongoClient[Mapping[str, Any]]
    db: Any
    node: Any
    blockchain: Any

    def __init__(self):
        self.db_instance = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.db_instance['Task1-version2']
        self.node = self.db['Node']
        self.blockchain = self.db['Blockchain']

    def insert_node(self, blockchain_type, ip, port, connection_status):
        node = NodeModel(blockchain_type, ip, port, connection_status)
        self.node.insert_one(node.set_node())

    def insert_blockchain(self, blockchain_type, active_connections, last_block, last_block_hash, confirmed_nodes_1, previous_block, previous_block_hash, confirmed_nodes_2, sent_messages, received_messages):
        blockchain_data = BlockchainModel(blockchain_type, active_connections, last_block, last_block_hash, confirmed_nodes_1, previous_block, previous_block_hash, confirmed_nodes_2, sent_messages, received_messages)
        self.blockchain.insert_one(blockchain_data.set_info())

    def delete_nodes(self):
        self.node.delete_many({})

    def update_node_status(self, ip, status):
        self.node.update_one({"ip_address": ip}, {"$set": {"connection_status": status}})
