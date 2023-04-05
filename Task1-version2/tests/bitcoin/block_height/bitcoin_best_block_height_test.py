import requests
import time

start = time.time()

block_hash = "00000000000000000002b2f7538a2b5e771149adccae9871f6d2a7e53b5007b7"

# Create the URL for the API request
block_height_message = f"https://blockstream.info/api/block/{block_hash}"

# Send the request and get the response
response = requests.get(block_height_message)

# Extract the block height from the response JSON
block_height = response.json()['height']

result = time.time() - start

# Print Results
print("Block hash:", block_hash)
print("Block height:", block_height)
print("Program time: ", result)
