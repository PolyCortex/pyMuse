from abc import ABC
from queue import Queue
from threading import Thread

from pymuse.constants import PIPELINE_QUEUE_SIZE


class PipelineStage(ABC, Thread):

    def __init__(self):
        super().__init__()
        self._queue_in: Queue = Queue(PIPELINE_QUEUE_SIZE)
        self._queues_out: list[Queue] = []

    @property
    def queue_in(self) -> Queue:
        return self._queue_in

    def add_queue_out(self, queue: Queue):
        self._queues_out.append(queue)

    def run(self):
        pass
