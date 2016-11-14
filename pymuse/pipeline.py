from utils import Thread, AutoQueue

from datetime import datetime
import time

import numpy as np


class Analyzer(Thread):
    def __init__(self, signal, window_duration, analysis_frequency=10.0, list_process=None, processes_to_visualize=None):
        """
        Constructor of analyzer. This class aims at providing the support for creating analysis pipeline for EEG data.
        
        :return:
        """
        super(Analyzer, self).__init__()
        self.name = 'analyzer'

        self.init_time = datetime.now()
        self.last_refresh = datetime.now()
        self.actual_refresh_frequency = analysis_frequency
        # self.last_save = datetime.now()

        self.signal = signal
        self.window_duration = window_duration

        self.analysis_frequency = analysis_frequency
        self.list_process_string = list_process
        self.list_process = {}
        if self.list_process_string is None:
            raise ValueError("No process has been to the list.")

        self.processes_to_visualize = processes_to_visualize
        self.list_viewer = {}

        self.number_of_process = len(self.list_process_string)
        self.queue_in = None
        self.queue_out = None

        self.prepare()

    def parse_process(self, process_name):
        bracket_open, bracket_close = process_name.find('('), process_name.find(')')
        process_param = {}
        if bracket_open != -1 and bracket_close != -1:
            split_comma = process_name[bracket_open+1:bracket_close].split(',')
            for spl in split_comma:
                split_equal = spl.split('=')
                process_param[split_equal[0]] = split_equal[1]
            return process_name[:bracket_open], process_param
        else:
            return process_name, process_param

    def prepare(self):
        list_queue = [AutoQueue(maxsize=1) for _ in range(self.number_of_process)]
        list_queue.append(AutoQueue(maxsize=100, autodrop=True))  # last queue has no limit
        self.queue_in = list_queue[0]
        self.queue_out = list_queue[-1]

        for i, process_name in enumerate(self.list_process_string):
            process_real_name, process_param = self.parse_process(process_name)
            mod = __import__('pymuse.processes', fromlist=[process_real_name])
            klass = getattr(mod, process_real_name)
            if process_param:
                self.list_process[process_real_name] = klass(list_queue[i], list_queue[i + 1], process_param)
            else:
                self.list_process[process_real_name] = klass(list_queue[i], list_queue[i + 1])

    def get_final_queue(self):
        return self.queue_out

    def start(self):
        for process_name in self.list_process:
            self.list_process[process_name].start()
        super(Analyzer, self).start()

    def display_alpha(self):
        while True:
            fft_signal = self.queue_out.get()
            if len(fft_signal.data) != 0:
                print np.mean(abs(fft_signal.data[:, 7:13]), axis=1)

    def refresh(self):
        for i, process_name in enumerate(self.processes_to_visualize):
            viewer_name = process_name + "Viewer"
            mod = __import__('pymuse.viz', fromlist=[viewer_name])
            klass = getattr(mod, viewer_name)
            self.list_viewer[process_name] = klass(refresh_freq=self.analysis_frequency,
                                                   label_channels=self.signal.label_channels)
            self.list_viewer[process_name].start()

        while True:
            time_now = datetime.now()
            seconds_passed = (time_now - self.last_refresh).total_seconds()
            if seconds_passed > 1.0 / self.analysis_frequency:
                self.actual_refresh_frequency = 1.0 / seconds_passed
                self.last_refresh = time_now
                pass
            else:
                time.sleep(0.001)
                continue

            print 'Pipeline frequency = ' + str(round(self.actual_refresh_frequency, 2)) + ' Hz'

            self.signal.lock.acquire()
            signal = self.signal.get_signal_window(length_window=self.window_duration)
            self.signal.lock.release()

            self.queue_in.put(signal, block=True, timeout=None)

            # refreshing viewers
            for process_name in self.list_viewer:
                if process_name == 'Raw':
                    self.list_viewer[process_name].refresh(signal)
                else:
                    if self.list_process[process_name].data is not None:
                        self.list_viewer[process_name].refresh(self.list_process[process_name].data)
