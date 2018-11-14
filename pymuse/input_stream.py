from pythonosc import dispatcher, osc_server
from datetime import datetime
from Queue import Queue

DEFAULT_PORT = 5001
LOCALHOST = '127.0.0.1'
DEFAULT_SIGNAL_QUEUE_LENGTH = 1024
DEFAULT_MUSE_EEG_ACQUISITION_FREQUENCY = 256
DEFAULT_MUSE_BATT_ACQUISITION_FREQUENCY = 10

class MuseInputStream():
    def __init__(self, port = DEFAULT_PORT, ip = LOCALHOST):
        self.signals = dict()
        disp = dispatcher.Dispatcher()
        disp.map("/eeg", self.callback, DEFAULT_MUSE_EEG_ACQUISITION_FREQUENCY, 'eeg')
        disp.map("/notch_filtered_eeg", self.callback, DEFAULT_MUSE_EEG_ACQUISITION_FREQUENCY, 'notch_filtered_eeg')
        disp.map("/batt", self.callback, DEFAULT_MUSE_BATT_ACQUISITION_FREQUENCY, 'batt')
        server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
        server.serve_forever()

    def callback(self, *args):
        data = []
        signal_name = args[-1]
        acquisition_frequency = args[-2]
        for arg in args[0:-2]:
            if(signal_name not in self.signals):
                self.signals[signal_name] = Signal(DEFAULT_SIGNAL_QUEUE_LENGTH, acquisition_frequency)
            data.append(arg)
        self.signals[signal_name].push(data)

class Signal():
    def __init__(self, length, acquisition_frequency):
        self.init_time = datetime.now()
        self.data = Queue(length)
        self.acquisition_period = 1/acquisition_frequency

    def push(self, data):
        self.data.put(data, True, self.acquisition_period)
    
    def pop(self):
        return self.data.get()
