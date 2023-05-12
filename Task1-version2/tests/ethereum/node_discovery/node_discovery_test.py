import csv
import json
import socket
import time

nodes_list = 'C:/Users/Admin/Desktop/Tu4k0/DL-Internship/Task1-version2/tests/ethereum/node_discovery/export-nodestrackerlist.csv'


def create_message(message):
    request_method = "POST / HTTP/1.1\r\n"
    host = f"Host: 192.168.0.100\r\n"
    content_type = f"Content-Type: application/json\r\n"
    content_length = f"Content-Length: {len(json.dumps(message))}\r\n\r\n{json.dumps(message)}"
    message = request_method + host + content_type + content_length

    return message.encode('utf-8')


def create_getblock_number_payload():
    method = 'eth_blockNumber'
    block_number_message = {
        'jsonrpc': '2.0',
        'method': method,
        'params': [],
        'id': '0',
    }

    return block_number_message


def create_getblock_hash_payload(block_number):
    method = 'eth_getBlockByNumber'
    block_hash_message = {
        'jsonrpc': '2.0',
        'id': '1',
        'method': method,
        'params': [hex(block_number), False]
    }

    return block_hash_message


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
            response = response[body_start:body_end-2] + '}' + '}'
            message.update(result=json.loads(response)['result'])
        else:
            body_end = response.rfind('}')
            message.update(result=json.loads(response[body_start:body_end + 1])['result'])

    return message


def get_best_block_hash(response) -> any:
    if len(response) != 0:
        best_block_hash = decode_response_message(response)['result']['hash']
    else:
        best_block_hash = None

    return best_block_hash


def get_best_block_number(response):
    if len(response) != 0:
        best_block_number = decode_response_message(response)['result']
        best_block_number = int(best_block_number, 16)
    else:
        best_block_number = None

    return best_block_number


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
    except OSError:
        pass


def receive_message(node):
    global amount_received_messages
    response = b''
    try:
        response = node.recv(4096)
    except OSError:
        pass
    finally:
        return response

def get_nodes(node_number):
    with open(nodes_list, 'r') as nodes:
        nodes = csv.reader(nodes)
        header = next(nodes)
        found_peers = dict()
        search_index = 0
        for node_info in nodes:
            if search_index == node_number + 1:
                break
            else:
                ip_address = node_info[2]
                ip_port = node_info[3]
                port = 8545
                node = set_socket()
                connect_node(node, ip_address, port)
                getblock_payload = create_getblock_number_payload()
                getblock_message = create_message(getblock_payload)
                send_message(node, getblock_message)
                response = receive_message(node)
                best_block_number = get_best_block_number(response)
                if isinstance(best_block_number, type(None)):
                    best_block_hash = None
                else:
                    getblockhash_payload = create_getblock_hash_payload(best_block_number)
                    getblockhash_message = create_message(getblockhash_payload)
                    send_message(node, getblockhash_message)
                    response = receive_message(node)
                    best_block_hash = get_best_block_hash(response)
                print(ip_address, ip_port)
                print('bb number: ', best_block_number)
                print('bb hash: ', best_block_hash)
                search_index += 1

    return found_peers


if __name__ == '__main__':
    start_time = time.time()
    nodes = get_nodes(200)
    print('Ethereum nodes list: ', nodes)
    execution_time = time.time() - start_time
    print("Program execution time: ", execution_time)