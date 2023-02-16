from application.btc_blockchain.btc_blockchain import BtcBlockchain
from application.eth_blockchain.eth_blockchain import EthBlockchain

if __name__ == '__main__':
    print('Service for manual node connection to Blockchain networks (BTC/ETH)')
    blockchain_name = input('Enter Blockchain name: ')
    if blockchain_name == 'BTC':
        BTC = BtcBlockchain(dns_seeds=[
            ("seed.bitcoin.sipa.be", 8333),
            ("dnsseed.bluematt.me", 8333),
            ("dnsseed.bitcoin.dashjr.org", 8333),
            ("seed.bitcoinstats.com", 8333),
            ("seed.bitnodes.io", 8333),
            ("bitseed.xf2.org", 8333),
        ])
        print('Socket info: ', BTC.set_socket())
        print('Peer node adress info: ', BTC.get_nodes_address())
        node = input('Enter node URL: ')
        port = input('Enter port: ')
        connection = BTC.connect_node(node=node, port=int(port))
        if connection:
            print('Connection status: True')
            version_request = BTC.create_message("version", BTC.create_version_message(node))
            BTC.send_message(version_request)
            version_response = BTC.receive_message()
            BTC.print_response('version', version_request, version_response)
            verack_response = BTC.receive_message()
            verack_request = BTC.create_message("verack", BTC.create_verack_message())
            BTC.send_message(verack_request)
            BTC.print_response('verack', verack_request, verack_response)
            getheaders_request = BTC.create_message("getheaders", BTC.create_getheaders_message())
            BTC.send_message(getheaders_request)
            getheaders_response = BTC.receive_message()
            BTC.print_response('getheaders', getheaders_request, getheaders_response)
            getdata_request = BTC.create_message("getdata", BTC.create_tx_getdata_message(
                '1dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e0000000000000000'))
            BTC.send_message(getdata_request)
            getdata_response = BTC.receive_message()
            BTC.print_response('getdata', getdata_request, getdata_response)
            getaddr_request = BTC.create_message("getaddr", BTC.create_getaddr_message())
            BTC.send_message(getaddr_request)
            getaddr_response = BTC.receive_message()
            BTC.print_response('getaddr', getaddr_request, getaddr_response)
            ping_request = BTC.create_message("ping", BTC.create_ping_message())
            BTC.send_message(ping_request)
            ping_response = BTC.receive_message()
            BTC.print_response('ping', ping_request, ping_response)
        else:
            exit()
    elif blockchain_name == 'ETH':
        ETH = EthBlockchain()
