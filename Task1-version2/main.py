import hashlib
import random
import socket
import struct
import time
from abc import abstractmethod, ABC


class BaseBlockchain(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def getData(self) -> dict:
        pass


class EthBlockchain(BaseBlockchain):

    def __init__(self):
        super().__init__()

    def getInfo(self):
        pass


class BtcBlockchain(BaseBlockchain):
    node: str
    sock: socket

    def __init__(self):
        super().__init__()

    def setSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if str(self.sock.type) == 'SocketKind.SOCK_STREAM':
            return self.sock
        else:
            return 0

    def getNodeAddresses(self):
        dns_seeds = [
            ("seed.bitcoin.sipa.be", 8333),
            ("dnsseed.bluematt.me", 8333),
            ("dnsseed.bitcoin.dashjr.org", 8333),
            ("seed.bitcoinstats.com", 8333),
            ("seed.bitnodes.io", 8333),
            ("bitseed.xf2.org", 8333),
        ]

        found_peers = []
        try:
            for (ip_address, port) in dns_seeds:
                for info in socket.getaddrinfo(ip_address, port,
                                               socket.AF_INET, socket.SOCK_STREAM,
                                               socket.IPPROTO_TCP):
                    found_peers.append((info[4][0], info[4][1]))
        except Exception:
            return found_peers

    def connectNode(self, node, port):
        try:
            print("Trying to connect to BTC node: ", node)
            self.sock.connect((node, port))
            return node
        except Exception:
            raise Exception('Node Url invalid')

    def createVersionMessage(self, node):
        version = struct.pack("i", 70015)
        services = struct.pack("Q", 0)
        timestamp = struct.pack("q", int(time.time()))
        add_recv_services = struct.pack("Q", 0)
        add_recv_ip = struct.pack(">16s", bytes(node, 'utf-8'))
        add_recv_port = struct.pack(">H", 8333)
        add_trans_services = struct.pack("Q", 0)
        add_trans_ip = struct.pack(">16s", bytes("127.0.0.1", 'utf-8'))
        add_trans_port = struct.pack(">H", 8333)
        nonce = struct.pack("Q", random.getrandbits(64))
        user_agent_bytes = struct.pack("B", 0)
        starting_height = struct.pack("i", 525453)
        relay = struct.pack("?", False)

        payload = version + services + timestamp + add_recv_services + add_recv_ip + add_recv_port + \
                  add_trans_services + add_trans_ip + add_trans_port + nonce + user_agent_bytes + starting_height + relay

        magic = bytes.fromhex("F9BEB4D9")

        command = b"version" + 5 * b"\00"
        length = struct.pack("I", len(payload))
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

        return magic + command + length + checksum + payload

    def encode_received_message(self, recv_message):
        recv_magic = recv_message[:4].hex()
        recv_command = recv_message[4:16]
        recv_length = struct.unpack("I", recv_message[16:20])
        recv_checksum = recv_message[20:24]
        recv_payload = recv_message[24:]
        recv_version = struct.unpack("i", recv_payload[:4])
        return (recv_magic, recv_command, recv_length, recv_checksum, recv_payload, recv_version)

    def getData(self):
        return self


if __name__ == '__main__':
    print('Service for manual node connection to Blockchain networks')
    blockchainName = input('Enter Blockchain name: ')
    if blockchainName == 'BTC':
        BTC = BtcBlockchain()
        BTC.setSocket()
        socketInfo = str(BTC.setSocket())
        print('BTC socket info: ', socketInfo)
        # print(BTC.getNodeAddresses())
        node = input('Enter node URL: ')
        port = input('Enter port: ')
        connection = BTC.connectNode(node=node, port=int(port))
        if connection:
            print('Connection status: True')
        verMessage = BTC.createVersionMessage(node)
        print('Send -Version- message to node')
        BTC.sock.send(verMessage)
        time.sleep(5)
        encoded_values = BTC.encode_received_message(BTC.sock.recv(8192))
        print("Version ping result: ", encoded_values[-1])