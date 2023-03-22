import threading


from application.btc_blockchain.btc_blockchain import BtcBlockchain

class Statistic:
    thread: threading.Thread
    connections: list = []
    requests: list
    responses: list

    def __init__(self):
        pass

    def collect_statistic(self):
        pass

    def set_active_connections(self):
        pass

    def get_active_connections(self):
        return len(self.connections)

    def get_requests(self, blockchain):
        return len(blockchain.requests)

