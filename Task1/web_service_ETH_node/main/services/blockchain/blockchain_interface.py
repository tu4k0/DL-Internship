from abc import abstractmethod, ABC
from web3 import Web3


class BaseBlockchain(ABC):

    @abstractmethod
    def __init__(self, nodeUrl: str):
        pass

    @abstractmethod
    def getBlockchainInfo(self) -> dict:
        pass


class EthDto:
    blockNumber: int
    price: int
    protocol: str
    id_chain: int
    hashrate: int
    mining: bool
    maxFee: int
    status: bool

    def __init__(self, blockNumber: int, price: int, protocol: str, id_chain: int, hashrate: int, mining: bool,
                 maxFee: int, status: bool) -> None:
        self.blockNumber = blockNumber
        self.price = price
        self.protocol = protocol
        self.id_chain = id_chain
        self.hashrate = hashrate
        self.mining = mining
        self.maxFee = maxFee


class EthBlockchain(BaseBlockchain, EthDto):

    def __init__(self, nodeUrl: str):
        super().__init__(nodeUrl)
        self.nodeUrl = nodeUrl
        self.web3 = Web3(Web3.HTTPProvider(self.nodeUrl))
        self.status = self.web3.isConnected()

    def getBlockchainInfo(self) -> EthDto:
        return EthDto(
            self.web3.eth.blockNumber,
            self.web3.eth.gas_price,
            self.web3.eth.protocol_version,
            self.web3.eth.chainId,
            self.web3.eth.hashrate,
            self.web3.eth.mining,
            self.web3.eth.max_priority_fee,
            self.web3.isConnected()
        )


class BtcDto:
    blockNumber: int
    price: int
    hashrate: int
    mempool: int

    def __init__(self, blockNumber: int, price: int, hashrate: int, mempool: int) -> None:
        self.blockNumber = blockNumber
        self.price = price
        self.hashrate = hashrate
        self.mempool = mempool


class BtcBlockchain(BaseBlockchain, BtcDto):

    def __init__(self, nodeUrl: str):
        super().__init__(nodeUrl)


    def getBlockchainInfo(self) -> BtcDto:
        return BtcDto(
            self.blockNumber,
            self.price,
            self.hashrate,
            self.mempool
        )
