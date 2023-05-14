import socket
from abc import abstractmethod, ABC


class BaseNode(ABC):
    node: socket
    ip: str
    port: int

    def __init__(self):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if str(self.node.type) == 'SocketKind.SOCK_STREAM':
            pass
        else:
            raise Exception('Failed to set socket')

    @abstractmethod
    def set_node(self):
        pass

    @abstractmethod
    def print_messages(self, data):
        pass

    def connect(self) -> str:
        self.node.settimeout(0.5)
        try:
            self.node.connect((self.ip, self.port))
        except TimeoutError:
            self.node.close()
        finally:
            return self.ip

    def get_connections(self):
        if self.node is None:
            raise Exception('Node not set yet')
        else:
            self.node.listen(1)
            conn, address = self.node.accept()
            while True:
                data = conn.recv(4096)
                if not data:
                    pass
                else:
                    self.print_messages(data)
