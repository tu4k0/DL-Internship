from application.base_blockchain.base_blockchain import BaseBlockchain


class EthBlockchain(BaseBlockchain):

    def __init__(self):
        super().__init__()

    def create_tx_getdata_message(self, tx_id) -> bytes:
        pass
