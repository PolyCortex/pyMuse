from abc import ABC
from queue import Empty
from threading import Thread, Event
from copy import deepcopy

from pymuse.utils.stoppablequeue import StoppableQueue
from pymuse.constants import PIPELINE_QUEUE_SIZE

TIMEOUT=0.1

class PipelineStage(ABC, Thread):
    """
    Abstract class that implements a pipeline stage. You must override the execute method and should
    implements the initialization_hook and shutdown_hook method.
    """
    def __init__(self):
        super().__init__()
        self._shutdown_event = Event()
        self._queue_in: StoppableQueue = StoppableQueue(PIPELINE_QUEUE_SIZE, self._shutdown_event)
        self._queues_out: list = []

    @property
    def queue_in(self) -> StoppableQueue:
        return self._queue_in

    def add_queue_out(self, queue=None):
        if queue is None:
            queue = StoppableQueue(self._shutdown_event, PIPELINE_QUEUE_SIZE)
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
        self._link_shutdown_event_with_queue_in()
        try:
            self._initialization_hook()
            while not(self.is_shutted_down()):
                self._execute()
        except SystemExit:
            pass

    def _link_shutdown_event_with_queue_in(self):
        if self._queue_in.shutdown_event is None:
            self._queue_in.shutdown_event = self._shutdown_event

    def _execute(self):
        """This is the method executed in loop in the pipeline stage's thread. You must override this function to do a custom PipelineStage."""
        pass
    
    def _initialization_hook(self):
        """ Override this method if you need an initialization routine before thread execution. """
        pass
