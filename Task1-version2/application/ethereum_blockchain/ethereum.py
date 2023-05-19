class Ethereum:
    network_id: int
    blockchain_type: str
    nodes_list: str
    nodes: dict
    best_block_hashes: list
    best_block_numbers: list
    prev_block_hashes: list
    prev_block_numbers: list
    amount_sent_messages: int
    amount_received_messages: int
    active_connections: int

    def __init__(self):
        self.network_id = 0
        self.blockchain_type = ''
        self.nodes_list = ''
        self.nodes = {}
        self.amount_sent_messages = 0
        self.amount_received_messages = 0
        self.best_block_hashes = []
        self.best_block_numbers = []
        self.prev_block_hashes = []
        self.prev_block_numbers = []
        self.active_connections = 0
