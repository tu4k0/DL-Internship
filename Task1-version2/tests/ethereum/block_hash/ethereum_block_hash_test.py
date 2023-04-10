import socket
import struct
import time
import requests
import rlp
import json


constant = {'peer_ip_address': '183.136.220.19',
             'peer_tcp_port': 8545,
             'buffer_size': 4096}


def make_message(message):
    request_method = "POST / HTTP/1.1\r\n"
    host = f"Host: 192.168.0.100\r\n"
    content_type = f"Content-Type: application/json\r\n"
    content_length = f"Content-Length: {len(json.dumps(message))}\r\n\r\n{json.dumps(message)}"
    message = request_method + host + content_type + content_length

    return message.encode('utf-8')


def create_getblock_number_message():
    method = 'eth_blockNumber'
    block_number_message = {
        'jsonrpc': '2.0',
        'method': method,
        'params': [],
        'id': '0',
    }

    return block_number_message

def create_getblock_hash_message():
    method = 'eth_getBlockByNumber'
    block_hash_message = {
        'jsonrpc': '2.0',
        'id': '1',
        'method': method,
        'params': ["latest", False]
    }

    return block_hash_message


def decode_response_message(response):
    response = response.decode('utf-8')
    message = {}
    status = message['status']=response[9:15]
    type = message['type']=response[43:47]
    length = message.update(length=len(response))
    body_start = response.find('{')
    body_end = response.rfind('}')
    body = message.update(result=json.loads(response[body_start:body_end + 1])['result'])

    return message


if __name__ == '__main__':
    start_time = time.time()

    # Create Messages
    getblock_payload = create_getblock_number_message()
    getblock_message = make_message(getblock_payload)
    getblockhash_payload = create_getblock_hash_message()
    getblockhash_message = make_message(getblockhash_payload)

    # Establish Node TCP Connection
    print('Setting connection')
    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node.connect((constant['peer_ip_address'], constant['peer_tcp_port']))

    #Send get block number message to ETH node
    print('send')
    node.send(getblock_message)

    #Retreiving result
    print('receive')
    result = node.recv(4096)

    node.send(getblockhash_message)
    print(node.recv(4096))

    #Show statistic
    print('Retreiving block hash data execution time: ', time.time()-start_time)
    print(result)
    print(decode_response_message(result)['result'])

    # Disconnect from node and Close the TCP connection
    node.close()
