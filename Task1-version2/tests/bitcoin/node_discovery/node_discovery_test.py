import binascii
import hashlib
import random
import socket
import struct
import time
import ipaddress

constant = {'magic_value': 0xd9b4bef9,
            'peer_ip_address': '156.245.20.1',
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


def handle_getaddr_message(node, response_data):
    found_nodes = {}
    getaddr = binascii.hexlify(response_data)
    getaddr_index = str(getaddr).find('616464720000000000000000')
    if len(getaddr[getaddr_index - 2:]) == 40:
        response_data += node.recv(constant['buffer_size'])
    node_discovery = binascii.hexlify(response_data)
    index = str(node_discovery).find('616464720000000000000000')
    node_info_size = 12
    adresses = node_discovery[index+44:]
    response_data = response_data[27:]
    while len(found_nodes) < node_number:
        node = binascii.hexlify(response_data[node_info_size:node_info_size + 16])
        if str(node).find('ffff') == -1:
            peer = ipaddress.IPv6Address(bytes(response_data[node_info_size:node_info_size + 16]))
            node_info_size += 30
        else:
            peer = str(ipaddress.IPv6Address(bytes(response_data[node_info_size:node_info_size + 16])).ipv4_mapped)
            port = binascii.hexlify(response_data[node_info_size + 16:node_info_size + 18])
            if int(port, 16) == 8333:
                found_nodes.update({peer: 8333})
            node_info_size += 30
    return found_nodes


if __name__ == '__main__':
    node_number = 5
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
    while True:
        if str(response_data).find('addr') != -1:
            found_peers = handle_getaddr_message(node, response_data)
            break
        else:
            response_data = node.recv(constant['buffer_size'])

    print(found_peers)
    print('Retreiving block hash data execution time: ', time.time() - start_time)

    node.close()
