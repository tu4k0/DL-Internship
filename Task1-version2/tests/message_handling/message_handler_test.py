import socket


class Node:
    socket: socket

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if str(self.socket.type) == 'SocketKind.SOCK_STREAM':
            pass
        else:
            raise Exception('Failed to set socket')

    def connect(self) -> socket.socket:
        self.socket.bind(('', 8333))

    def get_connections(self):
        if self.socket is None:
            raise Exception('Node not set yet')
        else:
            self.socket.listen(1)
            conn, address = self.socket.accept()
            while True:
                data = conn.recv(4096)
                if not data:
                    pass
                else:
                    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    print(node)
                    node.connect(('109.190.247.5', 8333))
                    node.send(data)
                    print(data)
                    response = node.recv(4096)
                    print(response)
                    conn.send(response)


if __name__ == '__main__':
    node = Node()
    node.connect()
    node.get_connections()