from application.application.app import CLI
from application.bitcoin_blockchain.bitcoin_p2p import BitcoinP2P


if __name__ == "__main__":
    bitcoin = BitcoinP2P()
    cli = CLI(bitcoin)
    cli.run()
