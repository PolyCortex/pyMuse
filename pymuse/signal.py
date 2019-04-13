from dataclasses import dataclass
from threading import Event

from pymuse.utils.stoppablequeue import StoppableQueue

@dataclass
class SignalData():
    """
    Dataclass for a signal data point. Event_marker attribute is optional
    """
    time: float
    values: list
    event_marker: list = None


class Signal():
    """Represents the accumulated signal that is store in a queue. It tag every sample with a time"""
    def __init__(self, length: int, acquisition_frequency: float):
        self._shutdown_event = Event()
        self._signal_queue: StoppableQueue = StoppableQueue(length, self._shutdown_event)
        self._signal_period: float = (1 / acquisition_frequency)
        self._data_counter: int = 0

    @property
    def signal_queue(self) -> StoppableQueue:
        return self._signal_queue

    def push(self, data_list: list):
        time = self._data_counter * self._signal_period
        signal_data: SignalData = SignalData(time, data_list)
        self._signal_queue.put(signal_data, True, self._signal_period)
        self._data_counter += 1

    def pop(self, timeout=None) -> SignalData:
        return self._signal_queue.get(True, timeout)

    def shutdown(self):
        self._shutdown_event.set()
