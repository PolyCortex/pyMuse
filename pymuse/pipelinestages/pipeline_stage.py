from abc import ABC
from queue import Queue
from threading import Thread, Event
from copy import deepcopy

from pymuse.constants import PIPELINE_QUEUE_SIZE


class PipelineStage(ABC, Thread):

    def __init__(self):
        super().__init__()
        self._queue_in: Queue = Queue(PIPELINE_QUEUE_SIZE)
        self._queues_out: list = []
        self._shutdown_event = Event()

    @property
    def queue_in(self) -> Queue:
        return self._queue_in

    def add_queue_out(self, queue: Queue):
        self._queues_out.append(queue)

    def _write_queues_out(self, data):
        for queue_out in self._queues_out:
            queue_out.put(deepcopy(data))

    # Override this method to correctly shutdown your pipeline stage
    def shutdown(self):
        """Kill the current module."""
        self._shutdown_hook()
        self._shutdown_event.set()

    def _shutdown_hook(self):
        """ Override this method if you need to safely shutdown the module."""
        pass

    def is_shutted_down(self) -> bool:
        return self._shutdown_event.is_set()

    def run(self):
        while not(self.is_shutted_down()):
            self.execute()

    def execute(self):
        "This is the method executed in loop in the pipeline stage's thread. You must override this function to do a custom PipelineStage."
        pass
