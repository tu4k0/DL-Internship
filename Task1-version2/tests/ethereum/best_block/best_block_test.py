import socket
import struct
import time
import requests
import rlp
import json


constant = {'peer_ip_address': '118.122.12.3',
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
        response = response[body_start:body_end-2] + '}' + '}'
        message.update(result=json.loads(response)['result'])
    else:
        body_end = response.rfind('}')
        message.update(result=json.loads(response[body_start:body_end + 1])['result'])

    return message


if __name__ == '__main__':
    start_time = time.time()

    # Create Message to get best block number
    getblock_payload = create_getblock_number_payload()
    getblock_message = create_message(getblock_payload)

    # Establish Node TCP Connection
    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node.connect((constant['peer_ip_address'], constant['peer_tcp_port']))

    #Send get block number message to ETH node
    node.send(getblock_message)

    #Retrieving response
    response = node.recv(constant['buffer_size'])
    best_block_number = int(decode_response_message(response)['result'], 16)

    # Create Message to get best block hash from received best number
    getblockhash_payload = create_getblock_hash_payload(best_block_number)
    getblockhash_message = create_message(getblockhash_payload)

    # Send get block hash message to ETH node
    node.send(getblockhash_message)

    # Retreiving result
    response = node.recv(constant['buffer_size'])
    best_block_hash = decode_response_message(response)['result']['hash']

    # Extract info about previous block
    prev_block_number = best_block_number - 1
    prev_block_hash = decode_response_message(response)['result']['parentHash']

    #Show statistic
    print('Retrieving Ethereum blockchain data execution time: ', time.time()-start_time)
    print('Best block number: ', best_block_number)
    print('Best block hash: ', best_block_hash)
    print('Prev block number: ', prev_block_number)
    print('Prev block hash: ', prev_block_hash)

    # Disconnect from node and Close the TCP connection
    node.close()
