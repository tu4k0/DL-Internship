import socket
import sys
import json
import unittest

constant = {'peer_ip_address': '183.36.220.19',
            'peer_tcp_port': 8545,
            'buffer_size': 4096}


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


def connect_node(node, ip_address, port):
    node.settimeout(3)
    try:
        node.connect((ip_address, port))
    except TimeoutError:
        node.close()
        sys.exit(1)
    finally:
        return True


def send_message(node, message):
    try:
        node.send(message)
    except OSError:
        pass


def receive_message(node):
    response = b''
    try:
        response = node.recv(constant['buffer_size'])
    except OSError:
        pass
    finally:
        return response


class Tests(unittest.TestCase):
    def test_ethereum_node_connection(self):
        listening_payload = create_net_listening_payload()
        listening_message = create_message(listening_payload)
        node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect_node(node, constant['peer_ip_address'], constant['peer_tcp_port'])
        send_message(node, listening_message)
        response = receive_message(node)
        status = handle_node_listening_status(response)
        node.close()
        self.assertIsNotNone(status)


if __name__ == '__main__':
    unittest.main()
