from utils import Thread, AutoQueue

from datetime import datetime, timedelta
import time

import numpy as np

import socket
from multiprocessing import Lock
from bisect import bisect_left


class InterfaceEvents(Thread):
    def __init__(self, udp_ip='127.0.0.1', udp_port='8888', message_size=16):
        super(InterfaceEvents, self).__init__()

        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.message_size = message_size

        self.list_events = AutoQueue(maxsize=250)
        self.list_events_time = AutoQueue(maxsize=250)

        self.lock = Lock()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.sock.bind((self.udp_ip, self.udp_port))

        # first message, with the sequence
        first_message, addr = self.sock.recvfrom(4096)  # buffer size is 1024 bytes

        self.frq_event, self.type_event, self.sequence_usage, self.sequence_training = self.decript_first_message(first_message)

    def get_nearest_message(self):
        pass

    def start(self):
        super(InterfaceEvents, self).start()

    def decript_first_message(self, m):
        message_split_by_type = m.split(' DONE')

        split_message = message_split_by_type[0].split(' ')
        frq_event = split_message[0]
        type_event = split_message[1]
        sequence_usage = split_message[2:]

        sequence_training = None
        if type_event == 'T':
            sequence_training_list = message_split_by_type[1].split(' ')[1:]
            sequence_training = [[sequence_training_list[2*i], sequence_training_list[2*i+1].split(',')] for i in range(len(sequence_training_list) / 2)]

        return frq_event, type_event, sequence_usage, sequence_training

    def add_event_synchronicity(self, time_event, event):
        self.lock.acquire()
        self.list_events.put(event)
        self.list_events_time.put(time_event)
        self.lock.release()

    def find_closest_event(self, datetime_window):
        event_usage, event_training = '', ''

        self.lock.acquire()
        list_events_time = list(self.list_events_time)
        list_events = list(self.list_events)
        self.lock.release()

        # search into the list of event and return the closest match
        index_closest_after = bisect_left(list_events_time, datetime_window)
        index_closest_before = index_closest_after - 1  # datetime are sorted in self.list_events_time

        datetime_before = list_events_time[index_closest_before]
        datetime_after = list_events_time[index_closest_before]
        index_event_before = list_events[index_closest_before]
        index_event_after = list_events[index_closest_before]

        # linear interpolation to find closest match
        percentage_closest = (datetime_window - datetime_before) / (datetime_after - datetime_before)
        index_event_closest = index_event_before + percentage_closest * (index_event_after - index_event_before)
        event_usage = self.sequence_usage[index_event_closest]

        # TODO: add extraction of usage for training

        return event_usage, event_training

    def refresh(self):
        while True:
            data, addr = self.sock.recvfrom(self.message_size)  # buffer size is 1024 bytes
            # data is a message with the structure:
            # message: TEMPS_CLOCK,INDEX
            # exemple: 2017-03-20 19:05:45.191179,42

            split_message = data.split(',')
            time_event = datetime.strptime(split_message[0], '%Y-%m-%d %H:%M:%S.%f')
            index_event = int(split_message[1])
            event = self.sequence_usage[index_event]

            # add event to a list
            self.add_event_synchronicity(time_event, event)


class Analyzer(Thread):
    def __init__(self, signal, window_duration, analysis_frequency=10.0, list_process=None, list_params=None,
                 processes_to_visualize=None, events_interface=None):
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

        # this offset can be used if synchronisation is difficult, in milliseconds
        # it moves in the past the sliding window, just to be sure it acquire a full window
        self.offset = 0.0

        self.signal = signal
        self.window_duration = window_duration

        self.analysis_frequency = analysis_frequency
        self.list_process_string = list_process
        self.list_process = []
        if self.list_process_string is None:
            raise ValueError("No process has been to the list.")
        self.list_params = list_params

        if len(self.list_params) != len(self.list_process_string):
            raise ValueError("List of parameters must have the same length as the list of processes.")

        self.processes_to_visualize = processes_to_visualize
        self.list_viewer = []

        self.number_of_process = len(self.list_process_string)
        self.queue_in = None
        self.queue_out = None

        self.messages = None  # Messages()

        self.events_interface = events_interface

        self.prepare_processes()
        self.initialize_interface()

    def prepare_processes(self):
        list_queue = [AutoQueue(maxsize=1) for _ in range(self.number_of_process)]
        list_queue.append(AutoQueue(maxsize=100, autodrop=True))  # last queue has no limit
        self.queue_in = list_queue[0]
        self.queue_out = list_queue[-1]

        for i, process in enumerate(self.list_process_string):
            if isinstance(process, str):
                mod = __import__('pymuse.processes', fromlist=[process])
                klass = getattr(mod, process)
                if self.list_params[i] is not None:
                    self.list_process.append(klass(list_queue[i], list_queue[i + 1], self.list_params[i]))
                else:
                    self.list_process.append(klass(list_queue[i], list_queue[i + 1]))
            else:
                process.queue_in = list_queue[i]
                process.queue_out = list_queue[i + 1]
                self.list_process.append(process)

    def initialize_interface(self):
        pass

    def get_final_queue(self):
        return self.queue_out

    def start(self):
        for i, process_name in enumerate(self.list_process):
            self.list_process[i].start()
        super(Analyzer, self).start()

    def refresh(self):
        for name in self.processes_to_visualize:
            if name == 'Raw':
                process_name = name
            else:
                process_name = self.list_process_string[name]
            viewer_name = process_name + "Viewer"
            mod = __import__('pymuse.viz', fromlist=[viewer_name])
            klass = getattr(mod, viewer_name)
            self.list_viewer.append(klass(refresh_freq=self.analysis_frequency, label_channels=self.signal.label_channels))
            self.list_viewer[-1].start()

        while True:
            try:
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

                time_start_window = datetime.now() - timedelta(milliseconds=self.window_duration) - timedelta(milliseconds=self.offset)

                self.signal.lock.acquire()
                signal = self.signal.get_signal_window(length_window=self.window_duration, time_start=time_start_window)
                self.signal.lock.release()

                if signal.data.shape[1] < 125:
                    continue

                self.queue_in.put(signal, block=True, timeout=None)

                # refreshing viewers
                for k, name in enumerate(self.processes_to_visualize):
                    if name == 'Raw':
                        self.list_viewer[k].refresh(signal)
                    else:
                        process_name = self.list_process_string[name]
                        if self.list_process[process_name].data is not None:
                            self.list_viewer[k].refresh(self.list_process[process_name].data)

            except KeyboardInterrupt:
                import sys
                print('KeyboardInterrupt on line {}'.format(sys.exc_info()[-1].tb_lineno))
                sys.exit(2)
            except Exception as e:
                import sys
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                print(str(e))
                sys.exit(2)
