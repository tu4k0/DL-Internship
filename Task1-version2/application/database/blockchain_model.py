class BlockchainModel:
    blockchain_type: str
    active_connections: int
    last_block: int
    last_block_hash: str
    confirmed_nodes_1: int
    previous_block: int
    previous_block_hash: str
    confirmed_nodes_2: int
    sent_messages: int
    received_messages: int
    created_at: str

    def __init__(
            self,
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
        self.blockchain_type = blockchain_type
        self.active_connections = active_connections
        self.last_block = last_block
        self.last_block_hash = last_block_hash
        self.confirmed_nodes_1 = confirmed_nodes_1
        self.previous_block = previous_block
        self.previous_block_hash = previous_block_hash
        self.confirmed_nodes_2 = confirmed_nodes_2
        self.sent_messages = sent_messages
        self.received_messages = received_messages
        self.created_at = created_at

    def set_info(self) -> dict:
        return dict({
            "blockchain_type": self.blockchain_type,
            "active_connections": self.active_connections,
            "last_block": self.last_block,
            "last_block_hash": self.last_block_hash,
            "confirmed_nodes_1": self.confirmed_nodes_1,
            "previous_block": self.previous_block,
            "previous_block_hash": self.previous_block_hash,
            "confirmed_nodes_2": self.confirmed_nodes_2,
            "sent_messages": self.sent_messages,
            "received_messages": self.received_messages,
            "created_at": self.created_at
        })