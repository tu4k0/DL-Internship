import binascii
import hashlib
import random
import socket
import struct
import time

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


def create_getdata_payload(tx_id):
    count = 1
    type = 1
    hash = bytearray.fromhex(tx_id)
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


# def getdata_message():
#     block_hash = '0000000000000000000549a764cc6f1ba850fe694249b87b41c54113e754d1c6'
#     count = struct.pack("<B", 1)
#     type = struct.pack("<L", 2)  # type : MSG_BLOCK
#     hash = struct.pack(">32s", block_hash.encode())  # need fix
#     inventory = type + hash
#
#     payload = count + inventory
#     return payload


# def print_response(command, request_data, response_data):
#     print("")
#     print("Command: " + command)
#     print("Request:")
#     print(binascii.hexlify(request_data))
#     print("Response:")
#     print(response_data)


def create_ping_payload() -> bytes:
    nonce = random.randint(1, 1 ** 32)
    payload = struct.pack('<Q', nonce)

    return payload


def create_getheaders_payload(start_block_header_hash):
    version = struct.pack("i", 70015)
    hash_count = struct.pack("<i", 1)
    hash_stop = bytes.fromhex("53A4CDB60C664DF2CAE6DCCAF8A9F2549BF526C85EFA02000000000000000000")
    block_locator_hashes = bytes.fromhex(start_block_header_hash)
    payload = version + hash_count + block_locator_hashes + hash_stop

    return payload


def create_getblocks_payload():
    version = struct.pack("i", 70015)
    hash_count = struct.pack("<i", 1)
    hash_stop = bytes.fromhex("000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd")
    start_block_header_hash = bytes.fromhex("00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048")
    payload = version + hash_count + start_block_header_hash + hash_stop

    return payload

def create_getblocks_message(start_block_hash=b'\x00'*32, end_block_hash=b'\x00'*32):
    version = struct.pack("<i", 70015)
    hash_count = struct.pack("<B", 1)
    start_block_hash = start_block_hash[::-1]
    end_block_hash = end_block_hash[::-1]
    payload = version + hash_count + start_block_hash + end_block_hash

    return payload

if __name__ == '__main__':
    start_time = time.time()

    # Create Messages
    version_payload = create_version_payload(constant['peer_ip_address'])
    version_message = create_message('version', version_payload)
    verack_message = create_verack_payload()
    getaddr_payload = create_getaddr_payload()
    getaddr_message = create_message('getaddr', getaddr_payload)
    # getdata_payload = create_getdata_payload('91b384fd2438e2d3664f97bf0fdfd4e8c87dac817fa16730717eee434b3e9f2b')
    # getdata_message = create_message('getdata', getdata_payload)
    # getblocks_payload = create_getblocks_payload()
    # getblocks_message = create_message('getblocks', getblocks_payload)
    getheaders_payload = create_getheaders_payload("4860eb18bf1b1620e37e9490fc8a427514416fd75159ab86688e9a8300000000")
    getheaders_message = create_message('getheaders', getheaders_payload)
    getheaders_payload2 = create_getheaders_payload("BC7A63D9881E1F544C9E98E2A22832FD0C1BFC1CD2BB05000000000000000000")
    getheaders_message2 = create_message('getheaders', getheaders_payload2)


    # Establish Node TCP Connection
    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node.connect((constant['peer_ip_address'], constant['peer_tcp_port']))

    # Send message "version"
    node.send(version_message)
    response_data = node.recv(constant['buffer_size'])
    print(response_data)
    time.sleep(2)

    # Send message "verack"
    node.send(verack_message)
    response_data = node.recv(constant['buffer_size'])
    print(response_data)
    time.sleep(2)

    # Send message "getaddr"
    node.send(getaddr_message)
    response_data = node.recv(constant['buffer_size'])
    print(response_data)
    time.sleep(2)

    # Send message "getheaders"
    node.send(getheaders_message)
    time.sleep(5)
    response_data = node.recv(constant['buffer_size'])
    print(response_data)

    # Send message "getheaders"
    node.send(getheaders_message2)
    time.sleep(5)
    response_data = node.recv(constant['buffer_size'])
    time.sleep(5)
    print(response_data)

    # Send message "getblocks"
    # node.send(getblocks_message)
    # time.sleep(5)
    # response_data = node.recv(constant['buffer_size'])
    # print(response_data)

    # Send message "getdata"
    # node.send(getdata_message)
    # print(node.recv(constant['buffer_size']))

