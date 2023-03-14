import os
import typer
import inquirer

from application.btc_blockchain.btc_blockchain import BtcBlockchain
from application.eth_blockchain.eth_blockchain import EthBlockchain


class CLI:
    app = typer.Typer()
    session_status: bool
    BTC: BtcBlockchain
    ETH: EthBlockchain
    node: str

    @app.command()
    def start_session():
        print('Service for manual node connection to Blockchain networks (BTC/ETH)')
        CLI.session_status = True
        while CLI.session_status:
            blockchain = inquirer.list_input("Choose option", choices=['bitcoin', 'ethereum', 'exit'])
            match blockchain:
                case 'bitcoin':
                    CLI.BTC = BtcBlockchain()
                    bitcoin_status = True
                    while bitcoin_status:
                        command = inquirer.list_input("Choose command",
                                                      choices=['connect-node', 'get-nodes', 'get-ip', 'set-node',
                                                               'disconnect-node', 'close'])
                        match command:
                            case 'connect-node':
                                print('Socket info: ', CLI.BTC.set_socket())
                                ip_address = typer.prompt('Enter node IP')
                                port = typer.prompt('Enter node port')
                                connection = CLI.BTC.connect_node(ip_address, port)
                                if connection:
                                    print('Connection status: True')
                                    print(f'Connected to BTC Node URL: {connection}:{port}')
                                    connection_status = True
                                    while connection_status:
                                        message = inquirer.list_input("Choose message",
                                                                      choices=['make-message', 'close'])
                                        match message:
                                            case 'make-message':
                                                message_status = True
                                                while message_status:
                                                    message_command = inquirer.list_input("Choose message command",
                                                                                          choices=['version', 'verack',
                                                                                                   'getheaders',
                                                                                                   'getdata', 'getaddr',
                                                                                                   'ping', 'close'])
                                                    match message_command:
                                                        case 'version':
                                                            request = CLI.BTC.make_message("version",
                                                                                           CLI.BTC.create_version_message(
                                                                                               ip_address))
                                                            CLI.__get_response_by_command(CLI, CLI.BTC, message_command,
                                                                                          request)
                                                        case 'verack':
                                                            request = CLI.BTC.make_message("verack",
                                                                                           CLI.BTC.create_verack_message())
                                                            CLI.__get_response_by_command(CLI, CLI.BTC, message_command,
                                                                                          request)
                                                        case 'getheaders':
                                                            request = CLI.BTC.make_message("getheaders",
                                                                                           CLI.BTC.create_getheaders_message())
                                                            CLI.__get_response_by_command(CLI, CLI.BTC, message_command,
                                                                                          request)
                                                        case 'getdata':
                                                            block = typer.prompt('Enter block hash')
                                                            request = CLI.BTC.make_message("getdata",
                                                                                           CLI.BTC.create_getdata_message(
                                                                                               block))
                                                            CLI.__get_response_by_command(CLI, CLI.BTC, message_command,
                                                                                          request)
                                                        case 'getaddr':
                                                            request = CLI.BTC.make_message("getaddr",
                                                                                           CLI.BTC.create_getaddr_message())
                                                            CLI.__get_response_by_command(CLI, CLI.BTC, message_command,
                                                                                          request)
                                                        case 'ping':
                                                            request = CLI.BTC.make_message("ping",
                                                                                           CLI.BTC.create_ping_message())
                                                            CLI.__get_response_by_command(CLI, CLI.BTC, message_command,
                                                                                          request)
                                                        case 'close':
                                                            message_status = False
                                                        case _:
                                                            print('Invalid BTC message command!')
                                            case 'close':
                                                connection_status = False
                                else:
                                    print('Connection Status: False')
                            case 'get-nodes':
                                node_num = int(typer.prompt('Enter nodes number'))
                                found_peers = CLI.BTC.get_nodes(node_num)
                                print('Peer nodes address info: ')
                                CLI.BTC.print_nodes(found_peers)
                            case 'get-ip':
                                print('Own IP:', CLI.BTC.get_ip())
                            case 'set_node':
                                print('Setting own node:', CLI.BTC.set_node())
                            case 'get-connections':
                                node_num = input('Enter number of simultaneously connected nodes: ')
                                print('Get ip of node connections:', CLI.BTC.get_connections(node_num))
                            case 'disconnect-node':
                                print(f'Disconnect from node: {CLI.BTC.ip_address}:{CLI.BTC.port}',
                                      CLI.BTC.disconnect_node())
                            case 'close':
                                bitcoin_status = False
                case 'ethereum':
                    CLI.ETH = EthBlockchain()
                    ethereum_status = True
                    while ethereum_status:
                        command = inquirer.list_input("Choose command",
                                                      choices=['connect-node', 'get-ip', 'set-node', 'disconnect-node',
                                                               'close'])
                        match command:
                            case 'connect-node':
                                print('Socket info: ', CLI.ETH.set_socket())
                                ip_address = input('Enter node URL: ')
                                port = int(input('Enter port: '))
                                connection = CLI.ETH.connect_node(ip_address, port)
                                if connection:
                                    print('Connection status: True')
                                    print(f'Connected to ETH Node URL: {connection}:{port}')
                                    connection_status = True
                                    while connection_status:
                                        message = inquirer.list_input("Choose message",
                                                                      choices=['make-message', 'close'])
                                        match message:
                                            case 'make-message':
                                                message_status = True
                                                while message_status:
                                                    message_command = inquirer.list_input("Choose message command",
                                                                                          choices=['getdata',
                                                                                                   'getblock',
                                                                                                   'getblock-tx-number',
                                                                                                   'getblock-number',
                                                                                                   'getnetwork',
                                                                                                   'getmining',
                                                                                                   'getbadblocks',
                                                                                                   'getgasprice',
                                                                                                   'ping', 'close'])
                                                    match message_command:
                                                        case 'getdata':
                                                            tx_hash = input('Enter transaction hash: ')
                                                            request = CLI.ETH.make_message(CLI.ETH.ip_address,
                                                                                           CLI.ETH.create_getdata_message(
                                                                                               tx_hash))
                                                            CLI.__get_response_by_command(CLI, CLI.ETH, message_command,
                                                                                          request)
                                                        case 'getblock':
                                                            block_number = int(typer.prompt('Enter block number'))
                                                            request = CLI.ETH.make_message(CLI.ETH.ip_address,
                                                                                           CLI.ETH.create_getblock_message(
                                                                                               block_number))
                                                            CLI.__get_response_by_command(CLI, CLI.ETH, message_command,
                                                                                          request)
                                                        case 'getblock-tx-number':
                                                            block_number = int(typer.prompt('Enter block number'))
                                                            request = CLI.ETH.make_message(CLI.ETH.ip_address,
                                                                                           CLI.ETH.create_getblock_tx_number_message(
                                                                                               block_number))
                                                            CLI.__get_response_by_command(CLI, CLI.ETH, message_command,
                                                                                          request)
                                                        case 'getblock-number':
                                                            request = CLI.ETH.make_message(CLI.ETH.ip_address,
                                                                                           CLI.ETH.create_getblock_number_message())
                                                            CLI.__get_response_by_command(CLI, CLI.ETH, message_command,
                                                                                          request)
                                                        case 'getnetwork':
                                                            request = CLI.ETH.make_message(CLI.ETH.ip_address,
                                                                                           CLI.ETH.create_getnetwork_message())
                                                            CLI.__get_response_by_command(CLI, CLI.ETH, message_command,
                                                                                          request)
                                                        case 'getmining':
                                                            request = CLI.ETH.make_message(CLI.ETH.ip_address,
                                                                                           CLI.ETH.create_getmining_message())
                                                            CLI.__get_response_by_command(CLI, CLI.ETH, message_command,
                                                                                          request)
                                                        case 'getbadblocks':
                                                            request = CLI.ETH.make_message(CLI.ETH.ip_address,
                                                                                           CLI.ETH.create_getbadblocks_message())
                                                            CLI.__get_response_by_command(CLI, CLI.ETH, message_command,
                                                                                          request)
                                                        case 'getgasprice':
                                                            request = CLI.ETH.make_message(CLI.ETH.ip_address,
                                                                                           CLI.ETH.create_getgasprice_message())
                                                            CLI.__get_response_by_command(CLI, CLI.ETH, message_command,
                                                                                          request)
                                                        case 'ping':
                                                            request = CLI.ETH.make_message(CLI.ETH.ip_address,
                                                                                           CLI.ETH.create_ping_message())
                                                            CLI.__get_response_by_command(CLI, CLI.ETH, message_command,
                                                                                          request)
                                                        case 'close':
                                                            message_status = False
                                                        case _:
                                                            print('Invalid ETH message command!')
                                            case 'close':
                                                connection_status = False
                                else:
                                    print('Connection Status: False')
                            case 'get-ip':
                                print('Own IP:', CLI.ETH.get_ip())
                            case 'set_node':
                                print('Setting own node:', CLI.ETH.set_node())
                            case 'get-connections':
                                node_num = typer.prompt('Enter number of simultaneously connected nodes')
                                print('Get ip of node connections:', CLI.ETH.get_connections(node_num))
                            case 'disconnect-node':
                                print(f'Disconnect from node: {CLI.ETH.ip_address}:{CLI.ETH.port}',
                                      CLI.ETH.disconnect_node())
                            case 'close':
                                ethereum_status = False
                case 'exit':
                    raise typer.Exit()

    @app.command()
    def end_session():
        os.system('taskkill /f /im cmd.exe')

    @app.command()
    def help():
        print('Help center of application commands description')
        CLI.help_status = True
        while CLI.help_status:
            parameter = inquirer.list_input("Choose option", choices=['socket', 'bitcoin', 'ethereum', 'exit'])
            match parameter:
                case 'socket':
                    print('SOCKET COMMANDS')
                    print('get-ip          :: \tReturns ip address of client')
                    print('set-socket      :: \tCreate new socket using the given address family, socket type and protocol number')
                    print('set-node        :: \tCreate node using the given address family, socket type and protocol number')
                    print('get-connections :: \tEnable server to accept node connections')
                    print('connect-node    :: \tConnect to remote node at address and port')
                    print('disconnect-node :: \tClose socket and terminate node connection')
                case 'bitcoin':
                    print('BTC COMMANDS')
                    print('make-message :: \tCreate client message (magic + command + length + checksum + payload) in byte format')
                    print('version      :: \tReturns node version')
                    print('verack       :: \tReturns node version acknowledgement')
                    print('getdata      :: \tReturns content of a specific object')
                    print('getaddr      :: \tReturns information about known active peers to help with finding potential nodes in the network')
                    print('ping         :: \tReturns proof that the TCP/IP connection is still valid')
                    print('getheaders   :: \tReturns headers packet containing the headers of blocks')
                case 'ethereum':
                    print('ETH COMMANDS')
                    print('make-message         :: \tCreate client message (POST + JSON ) in string format')
                    print('getdata              :: \tReturns information about tx requested by tx hash')
                    print('getblock             :: \tReturns information about a block by number')
                    print('getblock-tx-number   :: \tReturns number of tx in a block matching the given block number')
                    print('getblock-number      :: \tReturns number of most recent block')
                    print('getnetwork           :: \tReturns chain ID of current network')
                    print('getmining            :: \tReturns information about node mining status')
                    print('getbadblocks         :: \tReturns array of recent bad blocks that node seen in network')
                    print('getgasprice          :: \tReturns current price per gas in wei')
                    print('ping                 :: \tReturns information about node sync status')
                case 'exit':
                    CLI.help_status = False


    def __get_response_by_command(self, blockchain, message_command: str, request):
        blockchain.send_message(request)
        response = blockchain.receive_message()
        return blockchain.print_response(message_command, request, response)
