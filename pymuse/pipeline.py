from utils import Thread

from Queue import Queue
from datetime import datetime, timedelta
import time

import numpy as np

def timeTicks(x, pos):
    d = timedelta(milliseconds=x)
    return str(d)


class Analyzer(Thread):
    def __init__(self, signal, window_duration, analysis_frequency=10.0, list_process=None):
        """
        Constructor of analyzer. This class aims at providing the support for creating analysis pipeline for EEG data.
        
        :return:
        """
        super(Analyzer, self).__init__()
        self.name = 'analyzer'

        self.init_time = datetime.now()
        self.last_refresh = datetime.now()

        self.signal = signal
        self.window_duration = window_duration

        self.analysis_frequency = analysis_frequency
        self.list_process_string = list_process
        self.list_process = []
        if self.list_process_string is None:
            raise ValueError("No process has been to the list.")

        self.number_of_process = len(self.list_process_string)
        self.queue_in = None
        self.queue_out = None

        self.prepare()

    def prepare(self):
        list_queue = [[Queue(maxsize=1), Queue(maxsize=1)] for _ in self.list_process_string]
        self.queue_in = list_queue[0][0]
        self.queue_out = list_queue[-1][1]

        for i, process_name in enumerate(self.list_process_string):
            mod = __import__('pymuse.processes', fromlist=[process_name])
            klass = getattr(mod, process_name)
            self.list_process.append(klass(list_queue[i][0], list_queue[i][1]))

        import threading
        self.thread_display = threading.Thread(target=self.display_alpha)

    def get_final_queue(self):
        return self.queue_out

    def start(self):
        for process in self.list_process:
            process.start()
        super(Analyzer, self).start()

        self.thread_display.start()

    def display_alpha(self):
        while True:
            fft_signal = self.queue_out.get()
            if len(fft_signal.data) != 0:
                print np.mean(abs(fft_signal.data[:, 7:13]), axis=1)

    def refresh(self):
        while True:
            time_now = datetime.now()
            if (time_now - self.last_refresh).total_seconds() > 1.0 / self.analysis_frequency:
                self.last_refresh = time_now
                pass
            else:
                time.sleep(0.001)
                continue

            self.signal.lock.acquire()
            signal = self.signal.get_signal_window(length_window=self.window_duration)
            self.signal.lock.release()

            self.queue_in.put(signal, block=True, timeout=None)
