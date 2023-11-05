# Dl-Internship. Task1-version2

## Task Description
Development of a mini-node that makes a native connection with a P2P node of the blockchain network and monitors the information of network systems.  

## Project Reference
The service is a modular application presented in the form of interfaces:  
base_blockchain - abstract base class;  
btc_blockchain - Bitcoin class, contains the main methods for interaction and exchange of messages with the node through the P2P Mainnet network using sockets (PORT: 8333, MSG: magic + command + length + checksum);  
eth_blockchin - Ethereum class, contains basic methods for interaction and exchange of messages with a node through P2P Mainnet network using sockets (PORT: 8545, MSG: JSONRPC)  

## Project Tech Stack 
- Programming language: Python 3.10.10;
- CLI: CMD (sys.argv);  
- The mechanism for establishing a connection with a network node: Socket (TCP message request/response);  
- Ethereum messages: JSON-RPC;  
- Bitcoin messages: raw bytes (Bitcoin Core 70015);  
- Database: MongoDB;  
- Tests: unittests  

## To run the program
1. In cmd, under the link .../Task1-version2/ activate virtual environment: venv/Scripts/activate;  
2. Cd to Task1-version2/application/;  
3. Enter the command python main.py ip_address:port node_number  

## Supportable blockchains
- Bitcoin;  
- Ethereum;  
- Polygon;  
- BSC  

## Limitations and Scopes
In EVM-based blockchains nodes discovery process computes using pre-downloaded csv files. To download actual nodes data visit the link and download .csv:  
https://etherscan.io/nodetracker/nodes  
To search Bitcoin node address for initial connection use data from next source:  
https://bitnodes.io/nodes/?q=Satoshi:25.0.0  