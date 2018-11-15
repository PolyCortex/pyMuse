from pythonosc import dispatcher, osc_server
from datetime import datetime
from signal import Signal, SignalData
from muse_constants import ( 
    DEFAULT_MUSE_EEG_ACQUISITION_FREQUENCY, 
    DEFAULT_MUSE_BATT_ACQUISITION_FREQUENCY,
    MUSE_OSC_PATH,
    MUSE_ACQUISITION_FREQUENCIES,
)
from constants import ( 
    DEFAULT_PORT, 
    LOCALHOST,
    DEFAULT_SIGNAL_QUEUE_LENGTH,
)

class MuseInputStreamWrapper():
    signals: dict

    def __init__(self, sought_data_list: list<str> = ['eeg'], port: int = DEFAULT_PORT, ip: str = LOCALHOST):
        self.signals = dict()
        disp = dispatcher.Dispatcher()
        for sought_data in sought_data_list:
            disp.map(MUSE_OSC_PATH[sought_data], self.callback, MUSE_ACQUISITION_FREQUENCIES[sought_data], sought_data)
        server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
        server.serve_forever()

    def callback(self, osc_path, *registeredParams, *messages):
        data: SignalData = SignalData([], 0)
        acquisition_frequency = registeredParams[0]
        signal_name = registeredParams[1]
        for message in messages[2:]:
            if(signal_name not in self.signals):
                self.signals[signal_name] = Signal(DEFAULT_SIGNAL_QUEUE_LENGTH, acquisition_frequency)
            data.values.append(message)
        data.time = datetime.now() - self.signals[signal_name].init_time
        self.signals[signal_name].push(data)

    def get(self, signal_name: str):
        return self.signals[signal_name].pop()
