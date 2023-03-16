import threading


class NodeThread:

    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter

    def set_threads(self, node_number):
        threads = []
        for i in range(node_number):
            t = threading.Thread(target=please_sleep, args=[i])
            t.start()
            threads.append(t)

    def get_active_threads(self):
        return threading.active_count()
