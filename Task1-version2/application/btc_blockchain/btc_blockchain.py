import hashlib
import random
import socket
import struct
import time

from application.base_blockchain.base_blockchain import BaseBlockchain
from application.btc_blockchain.btc_config import *


class BtcBlockchain(BaseBlockchain):
    dns_seeds: list

    def __init__(self):
        super().__init__()
        self.requests = {}
        self.responses = {}
        self.commands = []

    def set_node(self):
        super().set_node()
        self.node.bind(('', btc_mainnet_port))

        return self.node

    def get_nodes(self, node_num) -> dict:
        found_peers = dict()
        search_index = 0
        found_peers.update({self.ip_address: self.port})
        try:
            for (ip_address, port) in dns_seeds:
                for info in socket.getaddrinfo(ip_address, port,
                                               socket.AF_INET, socket.SOCK_STREAM,
                                               socket.IPPROTO_TCP):
                    if search_index == node_num:
                        break
                    else:
                        found_peers.update({str(info[4][0]): info[4][1]})
                        search_index += 1
        except Exception:
            return found_peers

    def make_message(self, command, payload):
        magic = bytes.fromhex(btc_magic)
        command = bytes(command, 'utf-8') + (12 - len(command)) * b"\00"
        length = struct.pack("I", len(payload))
        if payload == '':
            check = b"\x5d\xf6\xe0\xe2"
        else:
            check = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        message = magic + command + length + check + payload

        return message

    def create_version_message(self, node_ip) -> bytes:
        version = 70015
        services = 1
        timestamp = int(time.time())
        addr_local = create_network_address("127.0.0.1", 8333)
        addr_peer = create_network_address(node_ip, 8333)
        nonce = random.getrandbits(64)
        start_height = 0
        payload = struct.pack('<LQQ26s26sQ16sL', version, services, timestamp, addr_peer,
                              addr_local, nonce, create_sub_version(), start_height)

        return payload

    def create_verack_message(self) -> bytearray:
        payload = bytearray.fromhex(verack_message)

        return payload

    def create_getdata_message(self, block_hash) -> bytes:
        count = 1
        type = 1
        hash = bytearray.fromhex(block_hash)
        payload = struct.pack('<bb32s', count, type, hash)

        return payload

    def create_getaddr_message(self) -> bytes:
        payload = b""

        return payload

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

    def create_getblocks_message(self, start_block_hash, end_block_hash):
        version = struct.pack("i", 70015)
        hash_count = struct.pack("<b", 1)
        hash_stop = bytes.fromhex(end_block_hash)
        start_block_header_hash = bytes.fromhex(start_block_hash)
        payload = version + hash_count + start_block_header_hash + hash_stop

        return payload

    def decode_response_message(self, message) -> tuple:
        message_magic = message[:4]
        message_command = message[4:16]
        # message_length = struct.unpack("I", message[16:20])
        # message_checksum = message[20:24]
        # message_payload = message[24:]

        return message_magic, message_command

    def execute_message(self, command_name: str, payload: list = None):
        if payload is not None:
            request = self.make_message(
                command_name,
                getattr(self, f'create_{command_name}_message')(payload)
            )
        else:
            request = self.make_message(command_name, getattr(self, f'create_{command_name}_message')())
        self.commands.append(command_name)
        self.requests.update({command_name: request})
        self.send_message(request)
        response = self.receive_message()
        if response is not None and not '':
            self.responses.update({command_name: response})
