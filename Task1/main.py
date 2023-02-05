from web3 import Web3, EthereumTesterProvider


def main():
    provider_url = 'https://mainnet.infura.io/v3/76510e6c5fd74be096e68fd41ba967a0'
    w3 = Web3(Web3.HTTPProvider(provider_url))
    print(w3.isConnected())
    print(w3.eth.blockNumber)


if __name__ == '__main__':
    main()
