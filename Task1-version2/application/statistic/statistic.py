import datetime


class Statistic:
    requests: int
    responses: int
    connections: list
    threads: list
    btc_blockchains_objects: list
    nodes: dict
    etc_blockchain_objects: list
    update_time: datetime.datetime

    def __init__(self):
        self.requests = 0
        self.responses = 0
        self.connections = []
        self.threads = []
        self.nodes = {}
        self.btc_blockchains_objects = []

    def show_blockchain_statistic(self):
        self.update_time = datetime.datetime.now()
        print('\nStatistics\n')
        print(f"Active connections: {len(self.connections)}\n")
        self.get_nodes_list()
        node_counter = 1
        for object in self.btc_blockchains_objects:
            print('\n')
            print('Node', node_counter, '  ', f'{object.ip_address},', object.port)
            print(f'{self.threads[node_counter - 1].name}: daemon-{self.threads[node_counter - 1].daemon}')
            node_counter += 1
            print(f"Commands {object.commands}:")
            print("Requests:")
            for request in object.requests:
                self.requests += 1
                print(request)
            print("Responses:")
            for response in object.responses:
                self.responses += 1
                print(response)
        print(f"\nTotal number of sent messages: {self.requests}")
        print(f"\nTotal number of received messages: {self.responses}")
        print(f"\nUpdated at: {self.update_time}")

    def get_nodes_list(self):
        print('Connected nodes list: ')
        if self.btc_blockchains_objects:
            node_counter = 1
            for object in self.btc_blockchains_objects:
                print('Node', node_counter, '  ', f'{object.ip_address},', object.port)
                node_counter += 1
        else:
            print('Failed to get node peers! Try again')
