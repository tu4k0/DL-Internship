import datetime


class Statistic:
    requests: int
    responses: int
    connections: list
    btc_blockchains_objects: list
    nodes: dict
    etc_blockchain_objects: list
    update_time: datetime.datetime

    def __init__(self):
        self.requests = 0
        self.responses = 0
        self.connections = []
        self.nodes = {}
        self.btc_blockchains_objects = []

    def show_blockchain_statistic(self):
        print('\nCollected Statistics\n')
        self.get_statistic_time()
        self.get_active_connections()
        self.get_nodes_list()
        self.get_nodes_statistic()
        self.get_requests_amount()
        self.get_responses_amount()

    def get_nodes_list(self):
        print('Connected nodes list: ')
        if self.btc_blockchains_objects:
            node_counter = 1
            for object in self.btc_blockchains_objects:
                print('Node', node_counter, '  ', f'{object.ip_address},', object.port)
                node_counter += 1
        else:
            print('Failed to get node peers! Try again')

    def get_nodes_statistic(self):
        node_counter = 1
        for object in self.btc_blockchains_objects:
            print('\n')
            print('Node', node_counter, '  ', f'{object.ip_address},', object.port)
            node_counter += 1
            print(f"Commands {object.commands}:")
            print("Requests:")
            for key, value in object.requests.items():
                self.requests += 1
                print(value)
            print("Responses:")
            for key, value in object.responses.items():
                self.responses += 1
                print(value)

    def get_active_connections(self):
        print(f"Active connections: {len(self.connections)}\n")

    def get_requests_amount(self):
        print(f"\nTotal number of sent messages: {self.requests}")

    def get_responses_amount(self):
        print(f"\nTotal number of received messages: {self.responses}")

    def get_statistic_time(self):
        self.update_time = datetime.datetime.now()
        print(f"Updated at: {self.update_time}\n")