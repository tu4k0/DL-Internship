import hashlib
import random
import socket
import struct
import time

from application.btc_blockchain.btc_config import *


# def make_message(command, payload):
#     magic = bytes.fromhex(btc_magic)
#     command = bytes(command, 'utf-8') + (12 - len(command)) * b"\00"
#     length = struct.pack("I", len(payload))
#     checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
#
#     return magic + command + length + checksum + payload
#
# def create_version_message(node_ip) -> bytes:
#     version = struct.pack("i", btc_version)
#     services = struct.pack("Q", 0)
#     timestamp = struct.pack("q", int(time.time()))
#     add_recv = struct.pack("Q", 0)
#     add_recv += struct.pack(">16s", bytes(node_ip, 'utf-8'))
#     add_recv += struct.pack(">H", 8333)
#     add_from = struct.pack("Q", 0)
#     add_from += struct.pack(">16s", bytes(host, 'utf-8'))
#     add_from += struct.pack(">H", 8333)
#     nonce = struct.pack("Q", random.getrandbits(64))
#     user_agent = struct.pack("B", 0)
#     height = struct.pack("i", 0)
#     payload = version + services + timestamp + add_recv + add_from + nonce + user_agent + height
#
#     return payload

def create_getdata_message():
    block_hash = '0000000000000000000549a764cc6f1ba850fe694249b87b41c54113e754d1c6'
    count = struct.pack("<B", 1)
    type = struct.pack("<L", 2)  # type : MSG_BLOCK
    hash = struct.pack(">32s", block_hash.encode())  # разобраться с этим или спросить у Богдана
    inventory = type + hash

    payload = count + inventory
    return payload


def create_version_message():
    version = struct.pack("i", 70015)
    services = struct.pack("Q", 0)
    timestamp = struct.pack("q", int(time.time()))
    addr_recv_services = struct.pack("Q", 0)
    addr_recv_ip = struct.pack(">16s", b"127.0.0.1")
    addr_recv_port = struct.pack(">H", 8333)
    addr_from_services = struct.pack("Q", 0)
    addr_from_ip = struct.pack(">16s", b"127.0.0.1")
    addr_from_port = struct.pack(">H", 8333)
    nonce = struct.pack("Q", random.getrandbits(64))
    user_agent_bytes = struct.pack("B", 0)
    start_height = struct.pack("i", 783053)
    relay = struct.pack("?", False)

    payload = version + services + timestamp + addr_recv_services + addr_recv_ip + addr_recv_port + addr_from_services + addr_from_ip + addr_from_port + nonce + user_agent_bytes + start_height + relay
    return payload


def create_verack_message():
    payload = bytearray.fromhex("f9beb4d976657261636b000000000000000000005df6e0e2")

    return payload

def create_getaddr_message():
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

def getdata_message():
    count = 1
    type = 1
    hash = bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000000')
    payload = struct.pack('<bb32s', count, type, hash)

    return payload

def create_ping_message() -> bytes:
    nonce = random.randint(1, 1 ** 32)
    payload = struct.pack('<Q', nonce)

    return payload

def create_getheaders_message(start_block_header_hash):
    version = struct.pack("i", 70015)
    hash_count = struct.pack("<b", 1)
    hash_stop = bytes.fromhex("00" * 32)
    payload = version + hash_count + start_block_header_hash + hash_stop
    return payload

def create_getblocks_message():
    version = struct.pack("i", 70015)
    hash_count = struct.pack("<b", 1)
    hash_stop = bytes.fromhex("00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048")
    start_block_header_hash = bytes.fromhex("000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd")
    payload = version + hash_count + start_block_header_hash + hash_stop
    return payload

# Connect to a Bitcoin node
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('100.36.127.250', 8333))
s.send(create_message("version", create_version_message()))
receive = s.recv(1024)
recv = s.recv(1024)
print('1',receive)
print('2', recv)
time.sleep(1)
s.send(create_message("verack", create_verack_message()))
time.sleep(1)
# s.send(create_message("getdata", getdata_message('1dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e0000000000000000')))
print('3', s.recv(1024))
# s.send(create_message("getaddr", create_getaddr_message()))
# res1 = s.recv(1024)
# res2 = s.recv(1024)
# print(res1)
# time.sleep(7)
s.send(create_message("getheaders", create_getheaders_message(bytes.fromhex("000000000000000000034ab50a4dea2037325fd160cb0e3bb2e1f7c580517ceb"))))
response = b""
while True:
    data = s.recv(1024)
    response+=data
    if len(data) < 1024:
        break
print('End while')
print(response)
time.sleep(3)
s.send(create_message("getdata", getdata_message()))
for i in range(1,41):
    print(s.recv(4096))
print('stop')
time.sleep(3)
print(s.recv(80))
# s.send(create_message("getheaders", create_getheaders_message(bytes.fromhex("000000000000000000034ab50a4dea2037325fd160cb0e3bb2e1f7c580517ceb"))))
# time.sleep(3)
# data = s.recv(1024)
# print(data)

