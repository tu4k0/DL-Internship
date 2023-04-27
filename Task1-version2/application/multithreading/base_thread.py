import threading

from abc import abstractmethod


class BaseThread(threading.Thread):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def clear_statistic(self):
        pass

    def stop(self):
        self.join()

    def get_thread_status(self):
        return self.is_alive()




