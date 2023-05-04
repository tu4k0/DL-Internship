import threading

from abc import abstractmethod, ABC


class BaseThread(threading.Thread, ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def run(self):
        pass

    def stop(self):
        self.join()

    def set_thread_name(self, name):
        self.name = name

    def get_thread_status(self):
        return self.is_alive()

    def get_active_threads(self):
        return threading.active_count()
