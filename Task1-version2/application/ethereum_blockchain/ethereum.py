class Ethereum:
    ip_address: str
    port: int
    node_number: int
    best_block_hash: str
    best_block_height: int
    previous_block_hash: str
    previous_block_height: int
    amount_sent_messages: int
    amount_received_messages: int
    active_connections: int

    def __init__(self, ip_address: str, port: int, node_number: int):
        self.ip_address = ip_address
        self.port = port
        self.node_number = node_number
        self.amount_sent_messages = 0
        self.amount_received_messages = 0

    def delete_ethereum(self):
        del self

