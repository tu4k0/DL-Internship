import hashlib
import random
import socket
import struct
import time
import requests

from application.base_blockchain.base_blockchain import BaseBlockchain


class BtcBlockchain(BaseBlockchain):
    node: str
    PORT: int
    socket: socket
    dns_seeds = [
        ("seed.bitcoin.sipa.be", 8333),
        ("dnsseed.bluematt.me", 8333),
        ("dnsseed.bitcoin.dashjr.org", 8333),
        ("seed.bitcoinstats.com", 8333),
        ("seed.bitnodes.io", 8333),
        ("bitseed.xf2.org", 8333),
    ]

    def __init__(self):
        super().__init__()

    def set_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if str(self.socket.type) == 'SocketKind.SOCK_STREAM':
            return self.socket
        else:
            return 0

    def get_ip(self):
        ip = requests.get('https://checkip.amazonaws.com').text.strip()
        return ip

    def set_node(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 8333))

    def get_connections(self, node_number):
        self.socket.listen(node_number)
        while True:
            user, addr = self.socket.accept()
            return user, addr

    def get_nodes_address(self) -> list:
        found_peers = []
        try:
            for (ip_address, port) in self.dns_seeds:
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

    def connect_node(self, node, port):
        try:
            print("Trying to connect to BTC node: ", node)
            self.socket.connect((node, port))
            return node
        except Exception:
            raise Exception('Node Url invalid')

    def disconnect_node(self):
        return self.socket.close()

    def create_message(self, command, payload):
        magic = bytes.fromhex('F9BEB4D9')
        command = bytes(command, 'utf-8') + (12 - len(command)) * b"\00"
        length = struct.pack("I", len(payload))
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        return magic + command + length + checksum + payload

    def create_version_message(self, node):
        version = struct.pack("i", 70015)
        services = struct.pack("Q", 0)
        timestamp = struct.pack("q", int(time.time()))

        add_recv = struct.pack("Q", 0)
        add_recv += struct.pack(">16s", bytes(node, 'utf-8'))
        add_recv += struct.pack(">H", 8333)

        add_from = struct.pack("Q", 0)
        add_from += struct.pack(">16s", bytes("192.168.0.100", 'utf-8'))
        add_from += struct.pack(">H", 8333)

        nonce = struct.pack("Q", random.getrandbits(64))
        user_agent = struct.pack("B", 0)
        height = struct.pack("i", 0)

        payload = version + services + timestamp + add_recv + add_from + nonce + user_agent + height

        return payload

    def create_verack_message(self):
        return bytearray.fromhex("f9beb4d976657261636b000000000000000000005df6e0e2")

    def create_tx_getdata_message(self, block_hash):
        count = 1
        type = 1
        hash = bytearray.fromhex(block_hash)
        payload = struct.pack('<bb32s', count, type, hash)
        return payload

    def create_getaddr_message(self):
        magic = bytes.fromhex("F9BEB4D9")
        command = b"getaddr" + 5 * b"\00"
        payload = b""
        length = struct.pack("I", len(payload))
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        return magic + command + length + checksum + payload

    def create_ping_message(self):
        nonce = random.randint(1, 1 ** 32)
        payload = struct.pack('<Q', nonce)
        return payload

    def create_getheaders_message(self):
        version = struct.pack("i", 70015)
        hash_count = struct.pack("i", 1)
        block_header_hashes = struct.pack('s', bytearray.fromhex("8C2ACBC70D503FDC36787AC0EE0916D4C504DD1624AA05000000000000000000"))
        stop_hash = b"0"
        payload = version + hash_count + block_header_hashes + stop_hash
        return payload

    def decode_message(self, message):
        message_magic = message[:4].hex()
        message_command = message[4:16]
        message_length = struct.unpack("I", message[16:20])
        message_checksum = message[20:24]
        message_payload = message[24:]
        return message_magic, message_command, message_length, message_checksum, message_payload

    def print_response(self, command, request_data, response_data):
        print("")
        print(f"Message: {command}")
        print("Program Request:")
        print(self.decode_message(message=request_data))
        print("Node response:")
        print(self.decode_message(message=response_data))