import sys

from bitcoin_blockchain.bitcoin_node import BitcoinNode

if __name__ == "__main__":
    try:
        blockchain = 'bitcoin'
        if blockchain == 'bitcoin':
            ip = '127.0.0.1'
            port = 8333
            light_node = BitcoinNode(ip, port)
            print('Start node!')
            light_node.set_node()
            print('Messages Data: ')
            light_node.get_connections()
    except KeyboardInterrupt:
        sys.exit('Stop node!')