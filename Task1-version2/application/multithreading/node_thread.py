import threading

from application.btc_blockchain.btc_blockchain import BtcBlockchain
from application.base_blockchain.base_blockchain import BaseBlockchain


class NodeThread(threading.Thread):
    threads = []
    sockets = []
    requests = []
    responses = []
    lock = threading.Lock()

    def __init__(self):
        super().__init__()

    def set_thread(self, nodes, blockchain):
        for key, value in nodes.items():
            blockchain.set_socket()
            connection = blockchain.connect_node(ip_address=key, port=value)
            self.sockets.append(connection)
            thread = threading.Thread(target=self.set_threads_function, args=(blockchain, key,))
            thread.start()
            print('\nNode: ', f'{key}:{value}')
            self.threads.append(thread)
            thread.join()

    def set_sockets(self, nodes):
        for key, value in nodes.items():
            sock = BtcBlockchain()
            socket = sock.set_socket()
            self.sockets.append(socket)
            print(sock.connect_node(ip_address=key, port=value))

    def print_sockets(self):
        return self.sockets

    def set_threads_function(self, blockchain, ip_address):
        self.lock.acquire()
        request = blockchain.make_message("version", blockchain.create_version_message(ip_address))
        blockchain.send_message(request)
        self.requests.append(request)
        response = blockchain.receive_message()
        self.responses.append(response)
        blockchain.print_response("version", request, response)
        self.lock.release()

    def stop_threads(self, nodes):
        for i in range(len(nodes)):
            self.threads[i].join()

    def get_active_threads(self):
        return self.threads

    def get_active_connections(self):
        return len(self.sockets)
