import sys

from bitcoin_blockchain.bitcoin_node import BitcoinNode

if __name__ == "__main__":
    bitcoin_light_node = BitcoinNode()
    try:
        print('Start Bitcoin node!')
        bitcoin_light_node.set_node()
        print(f'IP: {bitcoin_light_node.ip}')
        print(f'PORT: {bitcoin_light_node.port}')
        print('Messages Data: ')
        bitcoin_light_node.get_connections()
    except KeyboardInterrupt:
        bitcoin_light_node.disconnect()
        sys.exit('Stop node!')
