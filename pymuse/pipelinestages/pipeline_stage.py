from abc import ABC
from queue import Queue
from threading import Thread

from pymuse.constants import PIPELINE_QUEUE_SIZE


class PipelineStage(ABC, Thread):

    def __init__(self):
        super()
        self._queue_in: Queue = Queue(PIPELINE_QUEUE_SIZE)
        self._queues_out: list[Queue] = list()

    @property
    def queue_in(self) -> Queue:
        return self._queue_in

    def set_queue_out(self, queue: Queue, index: int = 0):
        self._queues_out[index] = queue

    def run(self):
        pass
