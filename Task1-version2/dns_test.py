import socket

dns_seeds = [
    ("seed.bitcoin.sipa.be", 8333),
    ("dnsseed.bluematt.me", 8333),
    ("dnsseed.bitcoin.dashjr.org", 8333),
    ("seed.bitcoinstats.com", 8333),
    ("seed.bitnodes.io", 8333),
]


# def get_nodes(node_num) -> dict:
#     found_peers = dict()
#     search_index = 0
#     try:
#         for (ip_address, port) in dns_seeds:
#             for info in socket.getaddrinfo(ip_address, port,
#                                            socket.AF_INET, socket.SOCK_STREAM,
#                                            socket.IPPROTO_TCP):
#                 if search_index == node_num:
#                     break
#                 else:
#                     found_peers.update({str(info[4][0]): info[4][1]})
#                     search_index += 1
#     except Exception:
#         return found_peers
#
#
# print(get_nodes(3))

#Вывести с первой записи socketaddr(адрес и порт) с днс команды по ее домену (пример:seed.bitcoin.sipa.be) и порту (пример:8333)
# print(dns_seeds[0][0], dns_seeds[0][1])
# print(socket.getaddrinfo(dns_seeds[0][0], dns_seeds[0][1])[1][4])

#Вывести с первой записи socketaddr(адрес и порт) со всех днс команд по ее домену (пример:seed.bitcoin.sipa.be) и порту (пример:8333)
# for ip_address, port in dns_seeds:
#     print(ip_address, port)
#     print(socket.getaddrinfo(ip_address, port)[0][4])

#Вывести все записи socketaddr(адрес и порт) со всех днс команд по ее домену
# for ip_address, port in dns_seeds:
#     print(ip_address, port)
#     for info in socket.getaddrinfo(ip_address, port):
#         print(info[4])