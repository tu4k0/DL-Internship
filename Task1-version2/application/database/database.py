import pymongo

from application.database.database_config import DB_DSN, DB_SCHEMA, DB_BLOCKCHAIN_COLLECTION, DB_NODE_COLLECTION
from application.database.node_model import NodeModel
from application.database.blockchain_model import BlockchainModel


class Database:
    db_instance = pymongo.MongoClient(DB_DSN)
    db = db_instance[DB_SCHEMA]
    node = db[DB_NODE_COLLECTION]
    blockchain = db[DB_BLOCKCHAIN_COLLECTION]

    @staticmethod
    def insert_node(
            blockchain_type: str,
            ip: str,
            port: int,
            connection_status: bool
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
            blockchain_type: str,
            active_connections: int,
            last_block: int,
            last_block_hash: str,
            confirmed_nodes_1: int,
            previous_block: int,
            previous_block_hash: str,
            confirmed_nodes_2: int,
            sent_messages: int,
            received_messages: int,
            created_at: str
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
    def delete_nodes(blockchain_type: str):
        Database.node.delete_many({'blockchain_type': blockchain_type})

    @staticmethod
    def delete_blockchain_info(blockchain_type: str):
        Database.blockchain.delete_many({'blockchain_type': blockchain_type})

    @staticmethod
    def update_node_status(ip: str, blockchain_type: str, status: bool):
        Database.node.update_one({
            "ip_address": ip,
            "blockchain_type": blockchain_type
        },
            {"$set": {"connection_status": status}})
