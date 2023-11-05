import socket
import json
import unittest

constant = {'peer_ip_address': '183.136.220.19',
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

def create_net_peer_count_payload():
    method = 'net_peerCount'
    net_peer_count_message = {
        'jsonrpc': '2.0',
        'method': method,
        'params': [],
        'id': '0'
    }

    return net_peer_count_message


class Tests(unittest.TestCase):
    def test_ethereum_messages(self):
        listening_payload = create_net_listening_payload()
        listening_message = create_message(listening_payload)
        peercount_payload = create_net_peer_count_payload()
        peercount_message = create_message(peercount_payload)
        node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node.connect((constant['peer_ip_address'], constant['peer_tcp_port']))
        node.send(listening_message)
        response = node.recv(constant['buffer_size'])
        node.send(peercount_message)
        response2 = node.recv(constant['buffer_size'])
        node.close()
        self.assertIsNotNone(response)
        self.assertIsNotNone(response2)


if __name__ == '__main__':
    unittest.main()
