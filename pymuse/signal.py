from threading import Lock
from datetime import datetime
from Queue import Queue

class Signal():
    def __init__(self, length, acquisition_frequency):
        self.init_time = datetime.now()
        self.lock = Lock()
        self.signals_queue = Queue(length)
        self.acquisition_period = 1 / acquisition_frequency

    def push(self, data):
        self.lock.acquire()
        self.signals_queue.put(data, True, self.acquisition_period)
        self.lock.release()
    
    def pop(self):
        self.lock.acquire()
        data = self.signals_queue.get(True)
        self.lock.release()
        return data
