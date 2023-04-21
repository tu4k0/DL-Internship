from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P


class Bitcoin:
    best_block_hash: str
    best_block_height: int
    previous_block_hash: str
    previous_block_height: int
    node: str
    amount_sent_messages: int
    amount_received_messages: int
    active_connections: int

    def __init__(self, bitcoin: BitcoinP2P):
        super().__init__()
        self.bitcoin = bitcoin
        
    def __del__(self):
        pass

    def __repr__(self):
        return list([BitcoinP2P,
                     self.best_block_hash,
                     self.best_block_height,
                     self.previous_block_hash,
                     self.previous_block_height,
                     self.node,
                     self.amount_sent_messages,
                     self.amount_received_messages,
                     self.active_connections
                     ])
