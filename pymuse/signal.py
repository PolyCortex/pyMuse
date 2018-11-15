from threading import Lock
from datetime import datetime
from PriorityQueue import PriorityQueue

class SignalData():
    time: float
    values: list

class Signal():
    init_time: float
    lock: Lock
    signals_queue: PriorityQueue
    acquisition_period: float

    def __init__(self, length: int, acquisition_frequency: float):
        self.init_time = datetime.now().timestamp()
        self.lock = Lock()
        self.signals_queue = PriorityQueue(length)
        self.acquisition_period = 1 / acquisition_frequency

    def push(self, data: SignalData):
        self.lock.acquire()
        self.signals_queue.put(data, True, self.acquisition_period)
        self.lock.release()
    
    def pop(self) -> SignalData:
        self.lock.acquire()
        data = self.signals_queue.get(True)
        self.lock.release()
        return data
