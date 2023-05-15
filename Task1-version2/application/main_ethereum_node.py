import sys

from ethereum_blockchain.ethereum_node import EthereumNode

if __name__ == "__main__":
    try:
        ethereum_light_node = EthereumNode()
        print('Start Ethereum node!')
        ethereum_light_node.set_node()
        print(f'IP: {ethereum_light_node.ip}')
        print(f'PORT: {ethereum_light_node.port}')
        print('Messages Data: ')
        ethereum_light_node.get_connections()
    except KeyboardInterrupt:
        sys.exit('Stop node!')
