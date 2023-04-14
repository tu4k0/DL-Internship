import requests

# replace with your node's IP address and port number
node_url = 'http://135.181.37.236:8545'

# retrieve the total number of peers connected to the node
payload = {"jsonrpc": "2.0", "id": 1, "method": "net_peerCount", "params": []}
response = requests.post(node_url, json=payload)
peer_count = int(response.json()['result'], 16)
print(peer_count)

# retrieve information about each connected peer, including IP address
for i in range(peer_count):
    payload = {"jsonrpc": "2.0", "id": i+1, "method": "net_peerState", "params": [hex(i)]}
    response = requests.post(node_url, json=payload)
    result = response.json()
    print(result)
