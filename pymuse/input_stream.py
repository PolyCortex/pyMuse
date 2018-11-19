from datetime import datetime
from signal import Signal, SignalData
from threading import Thread
from pythonosc import dispatcher, osc_server
from constants import DEFAULT_PORT, LOCALHOST, SIGNAL_QUEUE_LENGTH
from muse_constants import (
    MUSE_ACQUISITION_FREQUENCIES,
    MUSE_BATT_ACQUISITION_FREQUENCY,
    MUSE_EEG_ACQUISITION_FREQUENCY,
    MUSE_OSC_PATH,
)

class MuseInputStream():
    _signals: dict
    _server: osc_server.ThreadingOSCUDPServer

    def __init__(self, sought_data_list: list = ['eeg'], ip: str = LOCALHOST, port: int = DEFAULT_PORT):
        self._signals = dict()
        self._server = osc_server.ThreadingOSCUDPServer((ip, port), self._create_dispatchers(sought_data_list))
        Thread(target=self._server.serve_forever).start()

    def _callback(self, osc_path, opt_params, signal_data):
        signal_name = opt_params[0]
        self._signals[signal_name].push(signal_data)

    def _create_dispatchers(self, sought_data_list) -> dispatcher.Dispatcher:
        disp = dispatcher.Dispatcher()
        for sought_data in sought_data_list:
            if(sought_data not in self._signals):
                self._signals[sought_data] = Signal(SIGNAL_QUEUE_LENGTH, MUSE_ACQUISITION_FREQUENCIES[sought_data])
            disp.map(MUSE_OSC_PATH[sought_data], self._callback, sought_data)
        return disp

    def pop(self, signal_name: str) -> SignalData:
        return self._signals[signal_name].pop()

    def close(self):
        self._server.shutdown()
