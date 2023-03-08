import hashlib
import random
import socket
import struct
import time
import requests

from application.base_blockchain.base_blockchain import BaseBlockchain
from application.btc_blockchain.btc_config import *


class BtcBlockchain(BaseBlockchain):
    ip_address: str
    port: int
    socket: socket
    node: socket
    dns_seeds: list

    def __init__(self):
        super().__init__()

    def set_socket(self) -> socket.socket:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if str(self.socket.type) == 'SocketKind.SOCK_STREAM':
            return self.socket
        else:
            return 0

    def get_ip(self) -> str:
        ip = requests.get(ip_link).text.strip()
        return ip

    def set_node(self):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.node.bind(('', 8333))
        return self.node

    def get_connections(self, node_num) -> str:
        if self.node is None:
            raise Exception('Node not set yet')
        else:
            self.node.listen(node_num)
            conn, address = self.node.accept()
            print("Connection from: " + str(address))
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                return data

    def get_nodes_address(self) -> list:
        found_peers = []
        try:
            for (ip_address, port) in dns_seeds:
                for info in socket.getaddrinfo(
                        ip_address,
                        port,
                        socket.AF_INET,
                        socket.SOCK_STREAM,
                        socket.IPPROTO_TCP
                ):
                    found_peers.append((info[4][0], info[4][1]))
        except Exception:
            return found_peers

    def connect_node(self, ip_address, port) -> str:
        try:
            self.ip_address = ip_address
            self.port = int(port)
            self.socket.connect((self.ip_address, int(self.port)))
            return self.ip_address
        except Exception:
            raise Exception('Node Url invalid')

    def disconnect_node(self):
        return self.socket.close()

    def make_message(self, command, payload) -> bytes:
        magic = bytes.fromhex(btc_magic)
        command = bytes(command, 'utf-8') + (12 - len(command)) * b"\00"
        length = struct.pack("I", len(payload))
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        return magic + command + length + checksum + payload

    def create_version_message(self, node) -> bytes:
        version = struct.pack("i", btc_version)
        services = struct.pack("Q", 0)
        timestamp = struct.pack("q", int(time.time()))

        add_recv = struct.pack("Q", 0)
        add_recv += struct.pack(">16s", bytes(node, 'utf-8'))
        add_recv += struct.pack(">H", 8333)

        add_from = struct.pack("Q", 0)
        add_from += struct.pack(">16s", bytes(host, 'utf-8'))
        add_from += struct.pack(">H", 8333)

        nonce = struct.pack("Q", random.getrandbits(64))
        user_agent = struct.pack("B", 0)
        height = struct.pack("i", 0)

        payload = version + services + timestamp + add_recv + add_from + nonce + user_agent + height
        return payload

    def create_verack_message(self) -> bytearray:
        return bytearray.fromhex(verack_message)

    def create_getdata_message(self, block_hash) -> bytes:
        count = 1
        type = 1
        hash = bytearray.fromhex(block_hash)
        payload = struct.pack('<bb32s', count, type, hash)
        return payload

    def create_getaddr_message(self) -> bytes:
        magic = bytes.fromhex(btc_magic)
        command = b"getaddr" + 5 * b"\00"
        payload = b""
        length = struct.pack("I", len(payload))
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        return magic + command + length + checksum + payload

    def create_ping_message(self) -> bytes:
        nonce = random.randint(1, 1 ** 32)
        payload = struct.pack('<Q', nonce)
        return payload

    def create_getheaders_message(self) -> bytes:
        version = struct.pack("i", btc_version)
        hash_count = struct.pack("i", 1)
        block_header_hashes = struct.pack('s', bytearray.fromhex(block_header_hash))
        stop_hash = b"0"
        payload = version + hash_count + block_header_hashes + stop_hash
        return payload

    def send_message(self, message) -> int:
        return self.socket.send(message)

    def receive_message(self) -> bytes:
        return self.socket.recv(4096)

    def decode_message(self, message) -> tuple:
        message_magic = message[:4]
        message_command = message[4:16]
        message_length = struct.unpack("I", message[16:20])
        message_checksum = message[20:24]
        message_payload = message[24:]
        return message_magic, message_command, message_length, message_checksum, message_payload

    def print_response(self, command, request_data, response_data) -> None:
        print("")
        print(f"Message: {command}")
        print("Program Request:")
        print(self.decode_message(message=request_data))
        print("Node response:")
        print(self.decode_message(message=response_data))
