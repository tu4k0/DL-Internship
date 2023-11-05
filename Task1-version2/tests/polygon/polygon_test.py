import csv
import socket
import json
import unittest

nodes_list = 'C:/Users/Admin/Desktop/Tu4k0/DL-Internship/Task1-version2/tests/polygon/polygon-nodestrackerlist.csv'

constant = {'peer_ip_address': '74.118.136.75',
            'peer_tcp_port': 8545,
            'buffer_size': 4096}


def create_message(message: bytes) -> bytes:
    request_method = "POST / HTTP/1.1\r\n"
    host = f"Host: 192.168.0.100\r\n"
    content_type = f"Content-Type: application/json\r\n"
    content_length = f"Content-Length: {len(json.dumps(message))}\r\n\r\n{json.dumps(message)}"
    message = request_method + host + content_type + content_length

    return message.encode('utf-8')


def create_getblock_number_payload() -> any:
    method = 'eth_blockNumber'
    block_number_message = {
        'jsonrpc': '2.0',
        'method': method,
        'params': [],
        'id': '0',
    }

    return block_number_message


def create_getblock_hash_payload(block_number: int) -> any:
    method = 'eth_getBlockByNumber'
    block_hash_message = {
        'jsonrpc': '2.0',
        'id': '1',
        'method': method,
        'params': [hex(block_number), False]
    }

    return block_hash_message


def create_ping_payload() -> any:
    method = 'net_peerCount'
    ping = {
        'jsonrpc': '2.0',
        'id': '1',
        'method': method,
        'params': []
    }

    return ping


def create_version_payload() -> any:
    method = 'net_version'
    version_message = {
        'jsonrpc': '2.0',
        'id': '1',
        'method': method,
        'params': []
    }

    return version_message


def decode_response_message(response: bytes) -> any:
    response = response.decode('utf-8')
    message = {}
    status = message['status'] = response[9:15]
    type = message['type'] = response[43:47]
    length = message.update(length=len(response))
    body_start = response.find('{')
    if 'parentHash' in response:
        body_end = response.rfind('receiptsRoot')
        response = response[body_start:body_end - 2] + '}' + '}'
        message.update(result=json.loads(response)['result'])
    else:
        body_end = response.rfind('}')
        message.update(result=json.loads(response[body_start:body_end + 1])['result'])

    return message


def get_best_block_hash(response: bytes) -> any:
    if len(response) != 0:
        best_block_hash = decode_response_message(response)['result']['hash']
    else:
        best_block_hash = None

    return best_block_hash


def get_best_block_number(response: bytes) -> any:
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


def connect_node(node: socket.socket, ip_address: str, port: int):
    node.settimeout(0.5)
    try:
        node.connect((ip_address, port))
    except TimeoutError:
        node.close()
    finally:
        return ip_address


def send_message(node: socket.socket, message: str):
    global amount_sent_messages
    try:
        node.send(message)
    except OSError:
        pass


def receive_message(node: socket.socket) -> bytes:
    global amount_received_messages
    response = b''
    try:
        response = node.recv(4096)
    except OSError:
        pass
    finally:
        return response


def get_active_polygon_node() -> any:
    with open(nodes_list, 'r') as nodes:
        nodes = csv.reader(nodes)
        found_peer = []
        for node_info in nodes:
            ip_address = node_info[2]
            ip_port = node_info[3]
            port = 8545
            node = set_socket()
            connect_node(node, ip_address, port)
            ping_payload = create_ping_payload()
            ping_message = create_message(ping_payload)
            send_message(node, ping_message)
            response = receive_message(node)
            if response:
                found_peer.append(ip_address)
                found_peer.append(int(ip_port))
                return found_peer


class Tests(unittest.TestCase):
    def test_polygon(self):
        polygon_node = get_active_polygon_node()
        polygon_node[1] = int(8545)
        node = set_socket()
        connect_node(node, polygon_node[0], polygon_node[1])
        version_payload = create_version_payload()
        version_message = create_message(version_payload)
        send_message(node, version_message)
        response = receive_message(node)
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
