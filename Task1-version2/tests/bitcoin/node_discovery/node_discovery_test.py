import binascii
import hashlib
import random
import socket
import struct
import time
from threading import Event

constant = {'magic_value': 0xd9b4bef9,
             'peer_ip_address': '100.36.127.250',
             'peer_tcp_port': 8333,
             'buffer_size': 4096}


def create_sub_version():
    sub_version = "/Satoshi:0.24.1/"

    return b'\x0F' + sub_version.encode()


def create_network_address(ip_address, port):
    network_address = struct.pack('>8s16sH', b'\x01',
                                  bytearray.fromhex("00000000000000000000ffff") + socket.inet_aton(ip_address), port)

    return network_address

def create_version_payload(peer_ip_address):
    version = 70015
    services = 1
    timestamp = int(time.time())
    addr_local = create_network_address("127.0.0.1", 8333)
    addr_peer = create_network_address(peer_ip_address, 8333)
    nonce = random.getrandbits(64)
    start_height = 0
    payload = struct.pack('<LQQ26s26sQ16sL', version, services, timestamp, addr_peer,
                          addr_local, nonce, create_sub_version(), start_height)

    return payload


def create_verack_payload():
    payload = bytearray.fromhex("f9beb4d976657261636b000000000000000000005df6e0e2")

    return payload


def create_getaddr_payload():
    payload = b""
    return payload


def create_message(command, payload):
    magic = bytes.fromhex("F9BEB4D9")
    command = bytes(command, 'utf-8') + (12 - len(command)) * b"\00"
    length = struct.pack("I", len(payload))
    if payload == '':
        check = b"\x5d\xf6\xe0\xe2"
    else:
        check = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    message = magic + command + length + check + payload

    return message

def handle_getaddr_message(response):
    found_peers = []
    found_nodes = {}
    search_index = 0
    index = str(response).find("addr")
    if index != -1:
        response_data = node.recv(constant['buffer_size'])
        node_discovery = binascii.hexlify(response_data)[2:]
        near_nodes = node_discovery[:4].decode("utf-8")
        near_nodes_amount = bytearray.fromhex(near_nodes)
        near_nodes_amount.reverse()
        response_data = response_data[3:]
        nodes = binascii.hexlify(response_data)
        node_info_size = 60
        while len(found_nodes) < node_number:
            found_peers.append(nodes[:node_info_size])
            node_index = str(found_peers[search_index]).rfind("ffff")
            if node_index != -1:
                nodes = nodes[node_info_size:]
                found = found_peers[search_index][node_index + 2:node_index + 14]
                ip = found[:8]
                port = int(found[8:12], 16)
                if port == 8333:
                    address = ''
                    for i in range(0, len(ip), 2):
                        ip_address = int(ip[i:i + 2], 16)
                        address += f'{ip_address}.'
                    search_index += 1
                    found_nodes.update({address.rstrip('.'): port})
                else:
                    pass
            else:
                nodes = nodes[node_info_size:]
        return found_nodes


if __name__ == '__main__':
    node_number = int(input("Enter node number: "))
    start_time = time.time()

    # Create Messages
    version_payload = create_version_payload(constant['peer_ip_address'])
    version_message = create_message('version', version_payload)
    verack_message = create_verack_payload()
    getaddr_payload = create_getaddr_payload()
    getaddr_message = create_message('getaddr', getaddr_payload)


    # Establish Node TCP Connection
    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node.connect((constant['peer_ip_address'], constant['peer_tcp_port']))

    # Send message "version"
    node.send(version_message)
    response_data = node.recv(constant['buffer_size'])

    # Send message "verack"
    node.send(verack_message)
    response_data = node.recv(constant['buffer_size'])

    # Send message "getaddr"
    node.send(getaddr_message)
    response_data = node.recv(constant['buffer_size'])
    response_data = node.recv(constant['buffer_size'])
    response_data = node.recv(constant['buffer_size'])

    print(handle_getaddr_message(response_data))

    print('Retreiving block hash data execution time: ', time.time() - start_time)

    node.close()
