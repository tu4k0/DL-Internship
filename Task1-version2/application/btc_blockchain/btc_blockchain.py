import binascii
import hashlib
import random
import socket
import struct
import time
import requests

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

    def create_message(self, command, payload):
        magic = bytes.fromhex(btc_magic)
        command = bytes(command, 'utf-8') + (12 - len(command)) * b"\00"
        length = struct.pack("I", len(payload))
        if payload == '':
            check = b"\x5d\xf6\xe0\xe2"
        else:
            check = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        message = magic + command + length + check + payload

        return message

    def create_sub_version(self):
        sub_version = "/Satoshi:0.24.1/"

        return b'\x0F' + sub_version.encode()

    def create_network_address(self, ip_address, port):
        network_address = struct.pack('>8s16sH', b'\x01',
                                      bytearray.fromhex("00000000000000000000ffff") + socket.inet_aton(ip_address),
                                      port)

        return network_address

    def create_version_payload(self, node_ip) -> bytes:
        version = 70015
        services = 1
        timestamp = int(time.time())
        addr_local = self.create_network_address("127.0.0.1", 8333)
        addr_peer = self.create_network_address(node_ip, 8333)
        nonce = random.getrandbits(64)
        start_height = 0
        payload = struct.pack('<LQQ26s26sQ16sL', version, services, timestamp, addr_peer,
                              addr_local, nonce, self.create_sub_version(), start_height)

        return payload

    def create_verack_payload(self) -> bytearray:
        payload = bytearray.fromhex(verack_message)

        return payload

    def create_getdata_payload(self, block_hash) -> bytes:
        count = 1
        type = 1
        hash = bytearray.fromhex(block_hash)
        payload = struct.pack('<bb32s', count, type, hash)

        return payload

    def create_getaddr_payload(self) -> bytes:
        payload = b""

        return payload

    def create_ping_payload(self) -> bytes:
        nonce = random.randint(1, 1 ** 32)
        payload = struct.pack('<Q', nonce)

        return payload

    def create_getheaders_payload(self, start_block_hash) -> bytes:
        version = struct.pack("i", 70015)
        hash_count = struct.pack("<b", 1)
        block_locator_hashes = bytes.fromhex(start_block_hash)
        hash_stop = bytes.fromhex("00" * 32)
        payload = version + hash_count + block_locator_hashes + hash_stop

        return payload

    def create_getblocks_payload(self, start_block_hash, end_block_hash):
        version = struct.pack("i", 70015)
        hash_count = struct.pack("<b", 1)
        hash_stop = bytes.fromhex(end_block_hash)
        block_locator_hashes = bytes.fromhex(start_block_hash)
        payload = version + hash_count + block_locator_hashes + hash_stop

        return payload

    def create_getblock_height_payload(self, block_hash):
        getblock_height_message = f"https://blockstream.info/api/block/{block_hash}"
        response = requests.get(getblock_height_message)
        block_height = response.json()['height']

        return block_height

    def decode_getheaders_response(self, response) -> str:
        index = str(response).find("getheaders")
        if index == -1:
            getheaders = self.node.recv(4096)
            index = str(getheaders).find("getheaders")
            header = binascii.hexlify(getheaders)[index + 40:index + 104]
        else:
            header = binascii.hexlify(response)[140:204]

        block = header.decode("utf-8")
        block_hash = bytearray.fromhex(block)
        block_hash.reverse()

        return response.hex()

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
