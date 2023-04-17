import csv
import time

nodes_list = 'C:/Users/Admin/Desktop/Tu4k0/DL-Internship/Task1-version2/application/eth_blockchain/ethereum-nodestrackerlist.csv'


def get_nodes(node_number):
    with open(nodes_list, 'r') as nodes:
        nodes = csv.reader(nodes)
        found_peers = dict()
        search_index = 0
        for node_info in nodes:
            if search_index == node_number + 1:
                break
            else:
                if search_index == 0:
                    search_index += 1
                else:
                    found_peers.update({node_info[2]: 8545})
                    search_index += 1

    return found_peers


if __name__ == '__main__':
    start_time = time.time()
    nodes = get_nodes(100)
    print('Ethereum nodes list: ', nodes)
    execution_time = time.time() - start_time
    print("Program execution time: ", execution_time)