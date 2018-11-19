from dataclasses import dataclass
from datetime import datetime
from queue import PriorityQueue
from threading import Lock

@dataclass
class SignalData():
    time: float
    values: list

    def __lt__(self, other):
        return self.time < other.time

class Signal():
    signal_queue: PriorityQueue
    signal_period: float
    data_counter: int

    def __init__(self, length: int, acquisition_frequency: float):
        self.signal_queue = PriorityQueue(length)
        self.signal_period = (1 / acquisition_frequency)
        self.data_counter = 0

    def push(self, data_list: list):
        time = self.data_counter * self.signal_period
        signal_data: SignalData = SignalData(time, data_list)
        self.signal_queue.put(signal_data, True, self.signal_period)
        self.data_counter += 1
    
    def pop(self) -> SignalData:
        return self.signal_queue.get(True)
