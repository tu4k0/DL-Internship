import csv
import pandas as pd
from pathlib import Path

nodes_list = 'C:/Users/Admin/Desktop/Tu4k0/DL-Internship/Task1-version2/application/eth_blockchain/ethereum-nodestrackerlist.csv'


def get_nodes_list(nodes_list, node_number):
    with open(nodes_list, 'r') as csv_file:
        reader = csv.reader(csv_file)

        counter = 0

        for row in reader:
            if counter == node_number+1:
                break
            else:
                if counter == 0:
                    counter += 1
                else:
                    print(row[2])
                    counter += 1


if __name__ == '__main__':
    get_nodes_list(nodes_list, 5)