import socket
import time
import json


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


def handle_node_listening_status(response):
    response = str(response)
    status = str
    result_index = response.find("result")
    if result_index != -1:
        result = response[result_index+8:]
        status = result[:result.find("}")]
    return status


def connect_node(node, ip_address, port):
    try:
        node.connect((ip_address, port))
    except TimeoutError:
        node.close()
    finally:
        return ip_address


if __name__ == '__main__':
    start_time = time.time()

    # Create Messages
    listening_payload = create_net_listening_payload()
    listening_message = create_message(listening_payload)

    # Establish Node TCP Connection
    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect_node(node, constant['peer_ip_address'], constant['peer_tcp_port'])

    #Send get block number message to ETH node
    node.send(listening_message)

    #Retreiving response
    response = node.recv(constant['buffer_size'])
    status = handle_node_listening_status(response)

    #Show result
    print('Retrieving Ethereum blockchain data execution time: ', time.time()-start_time)
    print('Node listening status: ', status)

    # Disconnect from node and Close the TCP connection
    node.close()
