from abc import abstractmethod, ABC


class BaseBlockchain(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def getData(self, tx_id):
        pass
