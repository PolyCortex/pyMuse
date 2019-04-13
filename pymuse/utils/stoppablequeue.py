from threading import Event
from queue import Queue, Empty

TIMEOUT=0.1     

class StoppableQueue(Queue):
    def __init__(self, maxsize=0, shutdown_event: Event=None):
        super(StoppableQueue, self).__init__(maxsize)
        self.shutdown_event = shutdown_event

    def get(self, block=True, timeout=None):
        if self.shutdown_event is None:
            raise AttributeError('StoppableQueueException: Shutdown Event is not defined')

        if block and timeout is None:
            while not(self.shutdown_event.is_set()):
                try:
                    return super(StoppableQueue, self).get(True, TIMEOUT)
                except Empty:
                    pass
            raise SystemExit()            
        return super(StoppableQueue, self).get(block, timeout)
