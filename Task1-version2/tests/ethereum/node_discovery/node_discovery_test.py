import requests
from bs4 import BeautifulSoup
import time

node_tracker_link = 'https://etherscan.io/nodetracker/nodes'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}


def get_nodes(node_num):
    found_peers = dict()
    search_index = 1
    while len(found_peers) <= node_num:
        if node_num <= 50:
            r = requests.get(node_tracker_link, headers=headers)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                nodes = soup.find_all("tr")
                for node in nodes:
                    if len(found_peers) == node_num:
                        break
                    elif len(node.find_all('td')) != 0:
                        info = node.find_all('td')
                        found_peers.update({str(info[2].contents[0]): 8545})
            elif r.status_code == 403:
                raise Exception("The server understands the request but refuses to authorize it")
        else:
            r = requests.get(node_tracker_link, headers=headers, params={'p': str(node_num+search_index)})
            soup = BeautifulSoup(r.text, 'html.parser')
            nodes = soup.find_all("tr")
            for node in nodes:
                if len(found_peers) == node_num:
                    break
                elif len(node.find_all('td')) != 0:
                    info = node.find_all('td')
                    found_peers.update({str(info[2].contents[0]): 8545})

    return found_peers


if __name__ == '__main__':
    start_time = time.time()
    print(get_nodes(50))
    execution_time = time.time() - start_time
    print("Program execution time: ", execution_time)



