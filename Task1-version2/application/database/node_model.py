class NodeModel:
    blockchain_type: str
    ip_address: str
    port: int
    connection_status: bool

    def __init__(
            self,
            blockchain_type: str,
            ip: str,
            port: int,
            connection_status: bool
    ):
        self.blockchain_type = blockchain_type
        self.ip_address = ip
        self.port = port
        self.connection_status = connection_status

    def set_node(self) -> dict:
        return dict({
            "blockchain_type": self.blockchain_type,
            "ip_address": self.ip_address,
            "port": self.port,
            "connection_status": self.connection_status
        })
