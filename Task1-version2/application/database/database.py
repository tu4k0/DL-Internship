import pymongo

from application.database.node_model import NodeModel
from application.database.blockchain_model import BlockchainModel


class Database:
    db_instance = pymongo.MongoClient('mongodb://localhost:27017')
    db = db_instance['Task1-version2']
    node = db['Node']
    blockchain = db['Blockchain']

    @staticmethod
    def insert_node(
            blockchain_type,
            ip,
            port,
            connection_status
    ):
        node = NodeModel(
            blockchain_type,
            ip,
            port,
            connection_status
        )
        Database.node.insert_one(node.set_node())

    @staticmethod
    def insert_blockchain(
            blockchain_type,
            active_connections,
            last_block,
            last_block_hash,
            confirmed_nodes_1,
            previous_block,
            previous_block_hash,
            confirmed_nodes_2,
            sent_messages,
            received_messages,
            created_at
    ):
        blockchain_data = BlockchainModel(
            blockchain_type,
            active_connections,
            last_block,
            last_block_hash,
            confirmed_nodes_1,
            previous_block,
            previous_block_hash,
            confirmed_nodes_2,
            sent_messages,
            received_messages,
            created_at
        )
        Database.blockchain.insert_one(blockchain_data.set_info())

    @staticmethod
    def delete_nodes(blockchain_type):
        Database.node.delete_many({'blockchain_type': blockchain_type})

    @staticmethod
    def delete_blockchain_info(blockchain_type):
        Database.blockchain.delete_many({'blockchain_type': blockchain_type})

    @staticmethod
    def update_node_status(ip, port, status):
        Database.node.update_one({"ip_address": ip, "port": port}, {"$set": {"connection_status": status}})
