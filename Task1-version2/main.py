import binascii
import hashlib
import random
import socket
import struct
import time
import requests
from abc import abstractmethod, ABC

import re


class BaseBlockchain(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def getData(self, tx_id):
        pass


class EthBlockchain(BaseBlockchain):

    def __init__(self):
        super().__init__()

    def getInfo(self):
        pass


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

    def setSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if str(self.socket.type) == 'SocketKind.SOCK_STREAM':
            return self.socket
        else:
            return 0

    def getIp(self):
        ip = requests.get('https://checkip.amazonaws.com').text.strip()
        return ip

    def setNode(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 8333))

    def getConnections(self):
        self.socket.listen(5)
        while True:
            user, addr = self.socket.accept()
            return user, addr

    def getNodeAddresses(self) -> list:
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

    def connectNode(self, node, port):
        try:
            print("Trying to connect to BTC node: ", node)
            self.socket.connect((node, port))
            return node
        except Exception:
            raise Exception('Node Url invalid')

    def createVersionMessage(self, node):
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

    def createVerackMessage(self):
        return bytearray.fromhex("f9beb4d976657261636b000000000000000000005df6e0e2")

    def encodeReceivedMessage(self, recv_message):
        recv_magic = recv_message[:4].hex()
        recv_command = recv_message[4:16]
        recv_length = struct.unpack("I", recv_message[16:20])
        recv_checksum = recv_message[20:24]
        recv_payload = recv_message[24:]
        return (recv_magic, recv_command, recv_length, recv_checksum, recv_payload)

    def getData(self, block_hash):
        count = 1
        type = 1
        hash = bytearray.fromhex(block_hash)
        payload = struct.pack('<bb32s', count, type, hash)
        return payload

    def makeMessage(self, command, payload):
        magic = bytes.fromhex('F9BEB4D9')
        command = bytes(command, 'utf-8') + (12 - len(command)) * b"\00"
        length = struct.pack("I", len(payload))
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        return magic + command + length + checksum + payload

    def createGetAddrMessage(self):
        magic = bytes.fromhex("F9BEB4D9")
        command = b"getaddr" + 5 * b"\00"
        payload = b""
        length = struct.pack("I", len(payload))
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        return magic + command + length + checksum + payload

    def createPingMessage(self):
        nonce = random.randint(1, 1 ** 32)
        payload = struct.pack('<Q', nonce)
        return payload

    def createGetHeadersMessage(self):
        version = struct.pack("i", 70015)
        hash_count = struct.pack("i", 1)
        block_header_hashes = struct.pack('s', bytearray.fromhex("8C2ACBC70D503FDC36787AC0EE0916D4C504DD1624AA05000000000000000000"))
        stop_hash = b"0"
        payload = version + hash_count + block_header_hashes + stop_hash
        return payload

    def closeConnection(self):
        return self.socket.close()


if __name__ == '__main__':
    print('Service for manual node connection to Blockchain networks (BTC/ETH)')
    blockchainName = 'BTC'
    if blockchainName == 'BTC':
        BTC = BtcBlockchain()
        print(BTC.setSocket())
        print('BTC socket info: ', BTC.socket)
        print(BTC.getNodeAddresses())
        node = input('Enter node URL: ')
        port = input('Enter port: ')
        connection = BTC.connectNode(node=node, port=int(port))
        if connection:
            print('Connection status: True')
        print('Version message: ')
        request = BTC.makeMessage("version", BTC.createVersionMessage(node))
        print('Request:', request)
        BTC.socket.send(request)
        response = BTC.encodeReceivedMessage(BTC.socket.recv(1024))[1]
        print('Response: ', response)
        print('Verack message: ')
        verack_response = BTC.socket.recv(1024)
        print('Response: ', verack_response)
        verack_request = BTC.makeMessage("verack", BTC.createVerackMessage())
        BTC.socket.send(verack_request)
        print('Request: ', verack_request)
        print('GetHeadersBlocks: ')
        block_request = BTC.makeMessage("getheaders", BTC.createGetHeadersMessage())
        BTC.socket.send(block_request)
        print('Request: ', block_request)
        block_response = BTC.socket.recv(1024)
        print('Response: ', block_response)
        print('GetData: ')
        data = BTC.getData('1dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e0000000000000000')
        getdata_message = BTC.makeMessage('getdata', data)
        sendy = BTC.socket.send(getdata_message)
        rec = BTC.socket.recv(1024)
        print(getdata_message)
        print(rec)
        print('GetAddr: ')
        getAddr_request = BTC.createGetAddrMessage()
        BTC.socket.send(getAddr_request)
        print('Request: ', getAddr_request)
        getAddr_response = BTC.socket.recv(1024)
        print('Response: ', getAddr_response)
        print('Ping message: ')
        ping_request = BTC.makeMessage("ping", BTC.createPingMessage())
        BTC.socket.send(ping_request)
        print('Request: ', ping_request)
        ping_response = BTC.socket.recv(1024)
        print('Response: ', ping_response)
