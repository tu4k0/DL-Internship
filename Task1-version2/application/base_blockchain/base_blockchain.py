from abc import abstractmethod, ABC


class BaseBlockchain(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create_tx_getdata_message(self, tx_id) -> bytes:
        pass
