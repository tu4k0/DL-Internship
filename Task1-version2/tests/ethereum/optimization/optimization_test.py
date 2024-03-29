import csv
import socket
import sys
import time
import json
import threading
import unittest


def get_csv_file_path():
    file_path = __file__.split('\\')
    for i in range(len(file_path)):
        if file_path[i] == 'Task1-version2':
            result_path = file_path[:i+1]
    return '\\'.join(result_path) + '\\application\ethereum_blockchain\ethereum_based_nodes_lists\ethereum-nodestrackerlist.csv'


amount_sent_messages = 0
amount_received_messages = 0
nodes_list = get_csv_file_path()

def set_socket() -> socket.socket:
    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if str(node.type) == 'SocketKind.SOCK_STREAM':
        return node
    else:
        raise Exception('Failed to set socket')


def connect_node(node, ip_address, port):
    node.settimeout(0.5)
    try:
        node.connect((ip_address, port))
    except TimeoutError:
        node.close()
    finally:
        return ip_address


def send_message(node, message):
    global amount_sent_messages
    try:
        node.send(message)
        amount_sent_messages += 1
    except OSError:
        pass


def receive_message(node):
    global amount_received_messages
    response = b''
    try:
        response = node.recv(4096)
        amount_received_messages += 1
    except OSError:
        pass
    finally:
        return response


class NodeThread(threading.Thread):
    lock = threading.RLock()
    ip: str
    port: int
    best_block_numbers = []
    best_block_hashes = []
    prev_block_numbers = []
    prev_block_hashes = []
    amount_sent_messages = 0
    amount_received_messages = 0

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.name = ip

    def run(self):
        listening_payload = create_net_listening_payload()
        listening_message = create_message(listening_payload)
        node = set_socket()
        connection = connect_node(node, self.ip, self.port)
        if connection:
            send_message(node, listening_message)
            response = receive_message(node)
            status = handle_node_listening_status(response)
            if status == True:
                print('1', self.ip, self.port)
                best_block_number_payload = create_best_block_height_payload()
                best_block_number_message = create_message(best_block_number_payload)
                send_message(node, best_block_number_message)
                best_block_number_response = receive_message(node)
                best_block_number = get_best_block_number(best_block_number_response)
                best_block_hash_payload = create_getblock_by_number_payload(best_block_number)
                best_block_hash_message = create_message(best_block_hash_payload)
                send_message(node, best_block_hash_message)
                best_block_hash_response = receive_message(node)
                best_block_hash = get_best_block_hash(best_block_hash_response)
                self.best_block_hashes.append(best_block_hash)
                self.best_block_numbers.append(best_block_number)
                self.prev_block_numbers.append(best_block_number - 1)
                self.prev_block_hashes.append(get_previous_block_hash(best_block_hash_response))
            else:
                best_block_hash = None
                best_block_number = None
                prev_block_number = None
                prev_block_hash = None
                self.best_block_hashes.append(best_block_hash)
                self.best_block_numbers.append(best_block_number)
                self.prev_block_hashes.append(prev_block_hash)
                self.prev_block_numbers.append(prev_block_number)
            node.close()

    def collect_statistic(self):
        print("last block:\t", self.best_block_numbers[0], "\thash: ", self.best_block_hashes[0], "nodes: ",
              self.best_block_hashes.count(self.best_block_hashes[0]))
        print("previous block:\t", self.prev_block_numbers[0], "\thash: ", self.prev_block_hashes[0], "nodes: ",
              self.prev_block_hashes.count(self.prev_block_hashes[0]))
        print("total number of sent messages:\t\t", amount_sent_messages)
        print("total number of received messages:\t", amount_received_messages)

    def clear_statistic(self):
        self.best_block_numbers.clear()
        self.best_block_hashes.clear()
        self.prev_block_numbers.clear()
        self.prev_block_hashes.clear()


def get_nodes(ip_address, port, node_number):
    found_peers = dict()
    found_peers.update({ip_address: port})
    search_index = 0
    with open(nodes_list, 'r') as nodes:
        nodes = csv.reader(nodes)
        for node_info in nodes:
            if search_index == node_number:
                break
            else:
                if search_index == 0:
                    search_index += 1
                else:
                    found_peers.update({node_info[2]: 8545})
                    search_index += 1

    return found_peers


def create_message(message):
    request_method = "POST / HTTP/1.1\r\n"
    host = f"Host: 192.168.0.100\r\n"
    content_type = f"Content-Type: application/json\r\n"
    content_length = f"Content-Length: {len(json.dumps(message))}\r\n\r\n{json.dumps(message)}"
    message = request_method + host + content_type + content_length

    return message.encode('utf-8')


def create_net_listening_payload():
    method = 'net_listening'
    net_listening_message = {
        'jsonrpc': '2.0',
        'method': method,
        'params': [],
        'id': '0'
    }

    return net_listening_message


def create_getblock_by_number_payload(block_number):
    command = 'eth_getBlockByNumber'
    block_number_message = {
        'jsonrpc': '2.0',
        'method': command,
        'params': [hex(block_number), False],
        'id': '0'
    }

    return block_number_message


def create_best_block_height_payload():
    command = 'eth_blockNumber'
    best_block_height_message = {
        'jsonrpc': '2.0',
        'method': command,
        'params': [],
        'id': '0',
    }

    return best_block_height_message


def handle_node_listening_status(response):
    status = str
    if len(response) != 0:
        response = str(response)
        result_index = response.find("result")
        if result_index != -1:
            result = response[result_index + 8:]
            status = bool(result[:result.find("}")])
        return status
    else:
        status = False
        return False

def collect_ethereum_data_multithread(ip, port, node_number):
    nodes = get_nodes(ip, port, node_number)
    node_threads = []
    for ip, port in nodes.items():
        node = NodeThread(ip, port)
        node.start()
        node_threads.append(node)
    for node in node_threads:
        node.join()
    statistic_thread = NodeThread(None, None)
    statistic_thread.start()
    statistic_thread.collect_statistic()
    statistic_thread.clear_statistic()
    statistic_thread.join()
    time.sleep(2)
    delete_last_lines(5)


def decode_response_message(response):
    message = {}
    response = response.decode('utf-8')
    if not response:
        message.update(result=None)
    else:
        status = message['status'] = response[9:15]
        type = message['type'] = response[43:47]
        length = message.update(length=len(response))
        body_start = response.find('{')
        if 'transactions' in response:
            body_end = response.rfind('transactions')
            response = response[body_start:body_end - 2] + '}' + '}'
            message.update(result=json.loads(response)['result'])
        else:
            if response.rfind('parentHash') != -1:
                body_end = response.rfind('parentHash') + 80
                response = response[body_start:body_end] + '}' + '}'
                message.update(result=json.loads(response)['result'])
            else:
                body_end = response.rfind('}')
                message.update(result=json.loads(response[body_start:body_end + 1])['result'])

        return message


def get_best_block_hash(response):
    best_block_hash = decode_response_message(response)['result']['hash']

    return best_block_hash


def get_best_block_number(response):
    best_block_number = decode_response_message(response)['result']
    best_block_number = int(best_block_number, 16)

    return best_block_number


def get_previous_block_hash(response):
    previous_block_hash = decode_response_message(response)['result']['parentHash']

    return previous_block_hash


def delete_last_lines(n):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


class Tests(unittest.TestCase):
    def test_ethereum_optimization(self):
        ip_address = '65.109.22.107'
        port = 8545
        node_number = 3
        start = time.perf_counter()
        collect_ethereum_data_multithread(ip_address, port, node_number)
        end = time.perf_counter()
        self.assertLess(end-start, 3)


if __name__ == '__main__':
    unittest.main()
