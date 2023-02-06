from abc import abstractmethod, ABC
from web3 import Web3


class BaseBlockchain(ABC):

    @abstractmethod
    def setNodeUrl(self, nodeUrl: str) -> str:
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
        self.status = status


class EthBlockchain(BaseBlockchain, ABC, EthDto):
    nodeUrl: str
    blockNumber: int
    price: int
    protocol: int
    id_chain: int
    hashrate: int
    mining: bool
    maxFee: int
    web3: Web3

    def __init__(self, nodeUrl: str):
        self.nodeUrl = nodeUrl
        self.web3 = Web3(Web3.HTTPProvider(self.nodeUrl))

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
