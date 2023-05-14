import binascii
import socket
import sys
import time

import ipaddress

from application.bitcoin_blockchain.bitcoin_config import DNS_SEEDS, BITCOIN_GETADDR_COMMAND_HEX
from application.bitcoin_blockchain.bitcoin import Bitcoin
from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P
from application.bitcoin_blockchain.bitcoin_node_thread import BitcoinNodeThread
from application.bitcoin_blockchain.bitcoin_statistic import BitcoinStatistic


class BitcoinService:
    ip: str
    port: int
    node_number: int
    bitcoin: Bitcoin
    bitcoin_p2p: BitcoinP2P

    def __init__(self, user_request):
        self.bitcoin = Bitcoin()
        self.bitcoin_p2p = BitcoinP2P()
        self.ip = user_request[0]
        self.port = user_request[1]
        self.node_number = user_request[2]

    def start_session(self, user_request):
        ip_address = user_request[0]
        port = user_request[1]
        node_number = user_request[2]
        found_peers = {}
        version_payload = self.bitcoin_p2p.create_version_payload(ip_address)
        version_message = self.bitcoin_p2p.create_message('version', version_payload)
        verack_message = self.bitcoin_p2p.create_verack_payload()
        getaddr_payload = self.bitcoin_p2p.create_getaddr_payload()
        getaddr_message = self.bitcoin_p2p.create_message('getaddr', getaddr_payload)
        node = self.bitcoin_p2p.set_socket()
        connection = self.bitcoin_p2p.connect_node(node, ip_address, port)
        if connection:
            self.bitcoin_p2p.send_message(node, version_message)
            version_response = self.bitcoin_p2p.receive_message(node)
            if not version_response:
                sys.exit('Node not responding')
            self.bitcoin_p2p.send_message(node, verack_message)
            response_data = self.bitcoin_p2p.receive_message(node)
            self.bitcoin_p2p.send_message(node, getaddr_message)
            while True:
                if str(response_data).find('addr') != -1:
                    found_peers = self.get_nodes_from_getaddr(node, response_data, node_number, ip_address, port)
                    break
                else:
                    response_data = self.bitcoin_p2p.receive_message(node)
            node.close()
        while True:
            node_threads = []
            for ip, port in found_peers.items():
                node = BitcoinNodeThread(ip, port, self.bitcoin, self.bitcoin_p2p)
                node.start()
                node_threads.append(node)
            for node in node_threads:
                node.stop()
            bitcoin_statistic = BitcoinStatistic(self.bitcoin, self.bitcoin_p2p)
            bitcoin_statistic.set_amount_sent_messages()
            bitcoin_statistic.set_amount_received_messages()
            bitcoin_statistic.print_blockchain_info()
            time.sleep(5)
            bitcoin_statistic.clean_statistics()
            bitcoin_statistic.clear_statistic()

    def get_nodes_from_getaddr(self, node, response_data, node_number, ip_address, port):
        found_nodes = {}
        found_nodes.update({str(ip_address): port})
        getaddr = binascii.hexlify(response_data)
        getaddr_index = str(getaddr).find(BITCOIN_GETADDR_COMMAND_HEX)
        if len(getaddr[getaddr_index - 2:]) == 40:
            response_data += self.bitcoin_p2p.receive_message(node)
        node_info_size = 12
        response_data = response_data[27:]
        while len(found_nodes) < node_number:
            node = binascii.hexlify(response_data[node_info_size:node_info_size + 16])
            if str(node).find('ffff') == -1:
                peer = ipaddress.IPv6Address(bytes(response_data[node_info_size:node_info_size + 16]))
                port = binascii.hexlify(response_data[node_info_size + 16:node_info_size + 18])
                node_info_size += 30
            else:
                peer = str(ipaddress.IPv6Address(bytes(response_data[node_info_size:node_info_size + 16])).ipv4_mapped)
                port = binascii.hexlify(response_data[node_info_size + 16:node_info_size + 18])
                if int(port, 16) == 8333:
                    found_nodes.update({peer: 8333})
                node_info_size += 30

        return found_nodes

    def get_nodes_from_dns_seeds(self, node_number, ip_address, port) -> dict:
        found_peers = dict()
        search_index = 0
        found_peers.update({ip_address: port})
        try:
            for (ip_address, port) in DNS_SEEDS:
                for info in socket.getaddrinfo(ip_address, port,
                                               socket.AF_INET, socket.SOCK_STREAM,
                                               socket.IPPROTO_TCP):
                    if search_index == node_number:
                        break
                    else:
                        found_peers.update({str(info[4][0]): info[4][1]})
                        search_index += 1
        except Exception:
            raise Exception
        finally:
            return found_peers
