import socket
import unittest
import json

constant = {'peer_ip_address': '65.109.22.107',
            'peer_tcp_port': 8545,
            'buffer_size': 4096}


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
    response = response.decode('utf-8')
    message = {}
    status = message['status'] = response[9:15]
    type = message['type'] = response[43:47]
    length = message.update(length=len(response))
    body_start = response.find('{')
    if 'transactions' in response:
        body_end = response.rfind('transactions')
        response = response[body_start:body_end - 2] + '}' + '}'
        message.update(result=json.loads(response)['result'])
    else:
        body_end = response.rfind('}')
        message.update(result=json.loads(response[body_start:body_end + 1])['result'])

    return message


class Tests(unittest.TestCase):
    def test_ethereum_blocks(self):
        getblock_payload = create_getblock_number_payload()
        getblock_message = create_message(getblock_payload)
        node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node.connect((constant['peer_ip_address'], constant['peer_tcp_port']))
        node.send(getblock_message)
        response = node.recv(constant['buffer_size'])
        best_block_number = int(decode_response_message(response)['result'], 16)
        getblockhash_payload = create_getblock_hash_payload(best_block_number)
        getblockhash_message = create_message(getblockhash_payload)
        node.send(getblockhash_message)
        response = node.recv(constant['buffer_size'])
        best_block_hash = decode_response_message(response)['result']['hash']
        prev_block_number = best_block_number - 1
        prev_block_hash = decode_response_message(response)['result']['parentHash']
        node.close()
        self.assertGreater(best_block_number, 10000000)
        self.assertNotEqual(best_block_hash, prev_block_hash)
        self.assertNotEqual(best_block_number, prev_block_number)


if __name__ == '__main__':
    unittest.main()
