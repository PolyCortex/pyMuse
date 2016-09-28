import threading
from Queue import Queue


class AutoQueue(Queue, object):
    def __init__(self, **kwargs):
        self.autodrop = kwargs.pop('autodrop', None)
        super(AutoQueue, self).__init__(**kwargs)

    def put(self, item, block=False, timeout=None):
        if self.autodrop:
            if self.full():
                self.get()
        super(AutoQueue, self).put(item, block, timeout)


class Thread(object):
    def __init__(self):
        self.name = 'process_base'

        self.thread = threading.Thread(target=self.refresh)

    def refresh(self):
        print self.name, 'should never display this'
        pass

    def start(self):
        self.thread.start()
