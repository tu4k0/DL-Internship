import binascii
import hashlib
import random
import socket
import struct
import sys
import time
import threading
import ipaddress
import unittest
import requests

amount_sent_messages = 0
amount_received_messages = 0
constant = {'magic_value': 0xd9b4bef9,
            'peer_ip_address': '109.190.247.5',
            'peer_tcp_port': 8333,
            'buffer_size': 4096}


def set_socket() -> socket.socket:
    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if str(node.type) == 'SocketKind.SOCK_STREAM':
        return node
    else:
        raise Exception('Failed to set socket')


def connect_node(node, ip_address, port):
    node.settimeout(2)
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
        amount_sent_messages += 1
    except OSError:
        pass


def receive_message(node):
    global amount_received_messages
    response = b''
    try:
        response = node.recv(constant['buffer_size'])
        amount_received_messages += 1
    except OSError:
        pass
    except ConnectionAbortedError:
        pass
    except ConnectionResetError:
        pass
    finally:
        return response


class NodeThread(threading.Thread):
    lock = threading.RLock()
    ip: str
    port: int
    best_block_numbers = []
    best_block_hashes = []
    prev_block_numbers = []
    prev_block_hashes = []
    amount_sent_messages = 0
    amount_received_messages = 0

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.name = ip

    def run(self):
        node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection = connect_node(node, self.ip, self.port)
        if connection:
            version_payload = create_version_payload(constant['peer_ip_address'])
            version_message = create_message('version', version_payload)
            verack_message = create_verack_payload()
            getdata_payload = create_getdata_payload()
            getdata_message = create_message('getdata', getdata_payload)
            send_message(node, version_message)
            version_response = receive_message(node)
            if not version_response:
                best_block_hash = None
                best_block_number = None
                prev_block_number = None
                prev_block_hash = None
                self.best_block_hashes.append(best_block_hash)
                self.best_block_numbers.append(best_block_number)
                self.prev_block_hashes.append(prev_block_hash)
                self.prev_block_numbers.append(prev_block_number)
                node.close()
            else:
                send_message(node, verack_message)
                response_data = receive_message(node)
                send_message(node, getdata_message)
                while True:
                    if str(response_data).find('getheaders') != -1:
                        best_block_hash, prev_block_hash = handle_getheaders_message(node, response_data)
                        break
                    else:
                        response_data = receive_message(node)
                best_block_number = get_best_block_height(best_block_hash)
                self.best_block_hashes.append(best_block_hash)
                self.best_block_numbers.append(best_block_number)
                self.prev_block_numbers.append(best_block_number - 1)
                self.prev_block_hashes.append(prev_block_hash)

    def collect_statistic(self):
        print("last block:\t", self.best_block_numbers[0], "\thash: ", self.best_block_hashes[0], "nodes: ",
              self.best_block_hashes.count(self.best_block_hashes[0]))
        print("previous block:\t", self.prev_block_numbers[0], "\thash: ", self.prev_block_hashes[0], "nodes: ",
              self.prev_block_hashes.count(self.prev_block_hashes[0]))
        print("total number of sent messages:\t\t", amount_sent_messages)
        print("total number of received messages:\t", amount_received_messages)

    def clear_statistic(self):
        self.best_block_numbers.clear()
        self.best_block_hashes.clear()
        self.prev_block_numbers.clear()
        self.prev_block_hashes.clear()


def get_nodes(node, response_data, node_number, ip, port):
    found_nodes = {}
    found_nodes.update({str(ip):port})
    getaddr = binascii.hexlify(response_data)
    getaddr_index = str(getaddr).find('616464720000000000000000')
    if len(getaddr[getaddr_index - 2:]) == 40:
        response_data += receive_message(node)
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


def create_sub_version():
    sub_version = "/Satoshi:0.24.1/"

    return b'\x0F' + sub_version.encode()


def create_network_address(ip_address, port):
    network_address = struct.pack('>8s16sH', b'\x01',
                                  bytearray.fromhex("00000000000000000000ffff") + socket.inet_aton(ip_address), port)

    return network_address


def create_getdata_payload():
    count = 0
    type = 2
    hash = bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000000')
    payload = struct.pack('<bb32s', count, type, hash)

    return payload


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


def create_ping_payload() -> bytes:
    nonce = random.randint(1, 1 ** 32)
    payload = struct.pack('<Q', nonce)

    return payload


def create_getheaders_payload(start_block_header_hash):
    version = struct.pack("i", 70015)
    hash_count = struct.pack("<b", 1)
    hash_stop = bytes.fromhex("00" * 32)
    payload = version + hash_count + start_block_header_hash + hash_stop
    return payload


def create_getblocks_payload():
    version = struct.pack("i", 70015)
    hash_count = struct.pack("<b", 1)
    hash_stop = bytes.fromhex("00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048")
    start_block_header_hash = bytes.fromhex("000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd")
    payload = version + hash_count + start_block_header_hash + hash_stop
    return payload


def get_best_block_height(hash):
    block_height_message = f"https://blockstream.info/api/block/{hash}"
    response = requests.get(block_height_message)
    block_height = response.json()['height']
    return block_height


def collect_bitcoin_data_singlethread():
    found_peers = {}
    version_payload = create_version_payload(constant['peer_ip_address'])
    version_message = create_message('version', version_payload)
    verack_message = create_verack_payload()
    getaddr_payload = create_getaddr_payload()
    getaddr_message = create_message('getaddr', getaddr_payload)
    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = connect_node(node, constant['peer_ip_address'], constant['peer_tcp_port'])
    if connection:
        send_message(node, version_message)
        version_response = receive_message(node)
        if not version_response:
            sys.exit('Node not responding')
        send_message(node, verack_message)
        response_data = receive_message(node)
        send_message(node, getaddr_message)
        while True:
            if str(response_data).find('addr') != -1:
                found_peers = get_nodes(node, response_data, 3, constant['peer_ip_address'], constant['peer_tcp_port'])
                break
            else:
                response_data = receive_message(node)
        node.close()
    start_time = time.time()
    best_block_hashes = []
    best_block_numbers = []
    prev_block_hashes = []
    prev_block_numbers = []
    for ip, port in found_peers.items():
        node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection = connect_node(node, ip, port)
        if connection:
            version_payload = create_version_payload(constant['peer_ip_address'])
            version_message = create_message('version', version_payload)
            verack_message = create_verack_payload()
            getdata_payload = create_getdata_payload()
            getdata_message = create_message('getdata', getdata_payload)
            send_message(node, version_message)
            version_response = receive_message(node)
            if not version_response:
                best_block_hash = None
                best_block_number = None
                prev_block_number = None
                prev_block_hash = None
                best_block_hashes.append(best_block_hash)
                best_block_numbers.append(best_block_number)
                prev_block_hashes.append(prev_block_hash)
                prev_block_numbers.append(prev_block_number)
                node.close()
            else:
                send_message(node, verack_message)
                response_data = receive_message(node)
                send_message(node, getdata_message)
                while True:
                    if str(response_data).find('getheaders') != -1:
                        best_block_hash, prev_block_hash = handle_getheaders_message(node, response_data)
                        break
                    else:
                        response_data = receive_message(node)
                best_block_number = get_best_block_height(best_block_hash)
                best_block_hashes.append(best_block_hash)
                best_block_numbers.append(best_block_number)
                prev_block_numbers.append(best_block_number - 1)
                prev_block_hashes.append(prev_block_hash)


def collect_bitcoin_data_multithread():
    found_peers = {}
    version_payload = create_version_payload(constant['peer_ip_address'])
    version_message = create_message('version', version_payload)
    verack_message = create_verack_payload()
    getaddr_payload = create_getaddr_payload()
    getaddr_message = create_message('getaddr', getaddr_payload)
    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = connect_node(node, constant['peer_ip_address'], constant['peer_tcp_port'])
    if connection:
        send_message(node, version_message)
        version_response = receive_message(node)
        if not version_response:
            sys.exit('Node not responding')
        send_message(node, verack_message)
        response_data = receive_message(node)
        send_message(node, getaddr_message)
        while True:
            if str(response_data).find('addr') != -1:
                found_peers = get_nodes(node, response_data, 3, constant['peer_ip_address'], constant['peer_tcp_port'])
                break
            else:
                response_data = receive_message(node)
        node.close()
    start_time = time.time()
    node_threads = []
    for ip, port in found_peers.items():
        node = NodeThread(ip, port)
        node.start()
        node_threads.append(node)
    for node in node_threads:
        node.join()
    statistic_thread = NodeThread(None, None)
    statistic_thread.start()
    statistic_thread.collect_statistic()
    statistic_thread.clear_statistic()
    statistic_thread.join()


def handle_getheaders_message(node, response_data):
    getheaders = binascii.hexlify(response_data)
    getheaders_index = str(getheaders).find('676574686561646572730000')
    if len(getheaders[getheaders_index-2:]) == 40:
        response_data += node.recv(constant['buffer_size'])
    info = binascii.hexlify(response_data)
    index = str(info).find('676574686561646572730000')
    starting_hash = str(info)[index+50:]
    block_hash_size = 64
    block_hashes = []
    start_hash_index = 0
    for i in range(1,3):
        block_hashes.append(starting_hash[start_hash_index:block_hash_size])
        start_hash_index += 64
        block_hash_size += 64
    best_block_hash = bytearray.fromhex(block_hashes[0])
    best_block_hash.reverse()
    prev_block_hash = bytearray.fromhex(block_hashes[1])
    prev_block_hash.reverse()
    return best_block_hash.hex(), prev_block_hash.hex()


def delete_last_lines(n):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)

class Tests(unittest.TestCase):
    def test_bitcoin_singlethreading(self):
        start_time = time.time()
        collect_bitcoin_data_singlethread()
        end_time = time.time()
        self.assertGreater(end_time-start_time, 1)

    def test_bitcoin_multitheading(self):
        start_time = time.time()
        collect_bitcoin_data_multithread()
        end_time = time.time()
        self.assertLess(end_time - start_time, 5)


if __name__ == '__main__':
    unittest.main()
