from application.bitcoin_blockchain.bitcoin_p2p import BtcBlockchain


class Bitcoin(BtcBlockchain):
    best_block_hash: str
    best_block_height: int
    previous_block_hash: str
    previous_block_height: int
    node: str
    amount_sent_messages: int
    amount_received_messages: int
    active_connections: int

    def __int__(self):
        pass

    def __del__(self):
        pass

    def __repr__(self):
        return list([BtcBlockchain,
                     self.best_block_hash,
                     self.best_block_height,
                     self.previous_block_hash,
                     self.previous_block_height,
                     self.node,
                     self.amount_sent_messages,
                     self.amount_received_messages,
                     self.active_connections
                     ])
