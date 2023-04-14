from web3 import Web3

# create a web3 instance
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/76510e6c5fd74be096e68fd41ba967a0'))


latest_block = web3.eth.block_number
print(f"Latest block number: {latest_block}")

peers = web3.eth.getNodeInfo() # need research

print(f"List of connected peers: {peers}")
