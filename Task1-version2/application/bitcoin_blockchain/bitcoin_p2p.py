import hashlib
import random
import socket
import struct
import time

from application.base_blockchain.base_blockchain import BaseBlockchain
from application.bitcoin_blockchain.bitcoin_config import BITCOIN_MAINNET_VERSION, BITCOIN_MAINNET_PORT, BITCOIN_MAINNET_MAGIC, BITCOIN_DEFAULT_CHECKSUM, BITCOIN_USER_AGENT, BITCOIN_IPV4_SUBNET, BITCOIN_GENESIS_BLOCK


class BitcoinP2P(BaseBlockchain):
    dns_seeds: list

    def __init__(self):
        super(BitcoinP2P, self).__init__()

    def create_message(self, command, payload) -> bytes:
        magic = bytes.fromhex(BITCOIN_MAINNET_MAGIC)
        command = bytes(command, 'utf-8') + (12 - len(command)) * b"\00"
        length = struct.pack("I", len(payload))
        if payload == b"":
            checksum = BITCOIN_DEFAULT_CHECKSUM
        else:
            checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        message = magic + command + length + checksum + payload

        return message

    def create_version_payload(self, node_ip) -> bytes:
        version = BITCOIN_MAINNET_VERSION
        services = 1
        timestamp = int(time.time())
        addr_local = self.create_network_address(self.get_ip(), 8333)
        addr_peer = self.create_network_address(node_ip, 8333)
        nonce = random.getrandbits(64)
        start_height = 0
        payload = struct.pack('<LQQ26s26sQ16sL', version, services, timestamp, addr_peer,
                              addr_local, nonce, self.create_sub_version(), start_height)

        return payload

    def create_sub_version(self) -> bytes:
        return b'\x0F' + BITCOIN_USER_AGENT.encode()

    def create_network_address(self, ip_address, port) -> bytes:
        network_address = struct.pack('>8s16sH', b'\x01',
                                      bytearray.fromhex(BITCOIN_IPV4_SUBNET) + socket.inet_aton(ip_address),
                                      port)

        return network_address

    def create_verack_payload(self) -> bytes:
        packet_magic = bytes.fromhex(BITCOIN_MAINNET_MAGIC)
        command_name = bytes('verack', 'utf-8') + (12 - len('verack')) * b"\00"
        payload_length = bytes.fromhex('00000000')
        payload_checksum = bytes.fromhex('5df6e0e2')
        payload = packet_magic + command_name + payload_length + payload_checksum

        return payload

    def create_getdata_payload(self) -> bytes:
        count = 0
        type = 2
        hash = bytearray.fromhex(BITCOIN_GENESIS_BLOCK)
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
        version = struct.pack("i", BITCOIN_MAINNET_VERSION)
        hash_count = struct.pack("<b", 1)
        block_locator_hashes = bytes.fromhex(start_block_hash)
        hash_stop = bytes.fromhex("00" * 32)
        payload = version + hash_count + block_locator_hashes + hash_stop

        return payload

    def create_getblocks_payload(self, start_block_hash, end_block_hash) -> bytes:
        version = struct.pack("i", BITCOIN_MAINNET_VERSION)
        hash_count = struct.pack("<b", 1)
        hash_stop = bytes.fromhex(end_block_hash)
        block_locator_hashes = bytes.fromhex(start_block_hash)
        payload = version + hash_count + block_locator_hashes + hash_stop

        return payload
