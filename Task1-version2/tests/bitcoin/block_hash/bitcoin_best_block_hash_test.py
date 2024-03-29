import binascii
import hashlib
import random
import socket
import struct
import time
import unittest

constant = {'magic_value': 0xd9b4bef9,
            'peer_ip_address': '109.190.247.5',
            'peer_tcp_port': 8333,
            'buffer_size': 4096}


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


def handle_getheaders_message(node, response_data):
    getheaders = binascii.hexlify(response_data)
    getheaders_index = str(getheaders).find('676574686561646572730000')
    if len(getheaders[getheaders_index - 2:]) == 40:
        response_data += node.recv(constant['buffer_size'])
    info = binascii.hexlify(response_data)
    index = str(info).find('676574686561646572730000')
    starting_hash = str(info)[index + 50:]
    block_hash_size = 64
    block_hashes = []
    start_hash_index = 0
    for i in range(1, 3):
        block_hashes.append(starting_hash[start_hash_index:block_hash_size])
        start_hash_index += 64
        block_hash_size += 64
    best_block_hash = bytearray.fromhex(block_hashes[0])
    best_block_hash.reverse()
    prev_block_hash = bytearray.fromhex(block_hashes[1])
    prev_block_hash.reverse()
    return best_block_hash.hex(), prev_block_hash.hex()


class Tests(unittest.TestCase):
    def test_bitcoin_block_hash(self):
        version_payload = create_version_payload(constant['peer_ip_address'])
        version_message = create_message('version', version_payload)
        verack_message = create_verack_payload()
        getdata_payload = create_getdata_payload()
        getdata_message = create_message('getdata', getdata_payload)
        node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node.connect((constant['peer_ip_address'], constant['peer_tcp_port']))
        node.send(version_message)
        response_data = node.recv(constant['buffer_size'])
        node.send(verack_message)
        response_data = node.recv(constant['buffer_size'])
        node.send(getdata_message)
        while True:
            if str(response_data).find('getheaders') != -1:
                best_block_hash, prev_block_hash = handle_getheaders_message(node, response_data)
                break
            else:
                response_data = node.recv(constant['buffer_size'])
        self.assertNotEqual(best_block_hash, prev_block_hash)


if __name__ == '__main__':
    unittest.main()
