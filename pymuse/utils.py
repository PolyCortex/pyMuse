import threading


class Thread(object):
    def __init__(self):
        self.name = 'process_base'

        self.thread = threading.Thread(target=self.refresh)

    def refresh(self):
        print self.name, 'should never display this'
        pass

    def start(self):
        self.thread.start()
