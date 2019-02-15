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

    def __init__(self, length: int, acquisition_frequency: float):
        self._signal_queue: PriorityQueue = PriorityQueue(length)
        self._signal_period: float = (1 / acquisition_frequency)
        self._data_counter: int = 0

    @property
    def signal_queue(self) -> PriorityQueue:
        return self._signal_queue

    def push(self, data_list: list):
        time = self._data_counter * self._signal_period
        signal_data: SignalData = SignalData(time, data_list)
        self._signal_queue.put(signal_data, True, self._signal_period)
        self._data_counter += 1

    def pop(self) -> SignalData:
        return self._signal_queue.get(True)
