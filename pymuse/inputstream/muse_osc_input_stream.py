from threading import Thread
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pymuse.signal import Signal, SignalData
from pymuse.inputstream.constants import DEFAULT_UDP_PORT, LOCALHOST, SIGNAL_QUEUE_LENGTH
from pymuse.inputstream.muse_constants import (
    MUSE_ACQUISITION_FREQUENCIES,
    MUSE_OSC_PATH,
)

from time import time

class MuseOSCInputStream():

    def __init__(self, signal_name_list: list = ['eeg'], ip: str = LOCALHOST, port: int = DEFAULT_UDP_PORT):
        self._signals: dict = dict()
        self._server: ThreadingOSCUDPServer = ThreadingOSCUDPServer(
            (ip, port), self._create_dispatchers(signal_name_list))
        self.start_time = time()

    def _callback(self, osc_path, opt_params, *signal_data):
        print(time() - self.start_time)
        signal_name = opt_params[0]
        self._signals[signal_name].push(signal_data)

    def _create_dispatchers(self, signal_name_list: list) -> Dispatcher:
        disp = Dispatcher()
        for signal_name in signal_name_list:
            if(signal_name not in self._signals):
                self._signals[signal_name] = Signal(
                    SIGNAL_QUEUE_LENGTH, MUSE_ACQUISITION_FREQUENCIES[signal_name])
            disp.map(MUSE_OSC_PATH[signal_name], self._callback, signal_name)
        return disp

    def get_signal(self, signal_name: str) -> Signal:
        return self._signals[signal_name]

    def read(self, signal_name: str) -> SignalData:
        return self._signals[signal_name].pop()

    def start(self):
        Thread(target=self._server.serve_forever).start()

    def close(self):
        self._server.shutdown()
