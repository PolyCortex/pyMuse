from threading import Thread
from queue import Full
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.dispatcher import Dispatcher

from pymuse.signal import Signal, SignalData
from pymuse.inputstream.constants import DEFAULT_UDP_PORT, LOCALHOST, SIGNAL_QUEUE_LENGTH
from pymuse.inputstream.muse_constants import (
    MUSE_ACQUISITION_FREQUENCIES,
    MUSE_OSC_PATH,
)


class MuseOSCInputStream():
    """ 
    Creates an OSC/UDP server that runs on a new thread. It receives and enqueues every data that you
    specify in the constructor (see muse_constants.py).
    """

    def __init__(self, signal_name_list: list = ['eeg'], ip: str = LOCALHOST, port: int = DEFAULT_UDP_PORT):
        self._signals: dict = dict()
        self._server: ThreadingOSCUDPServer = ThreadingOSCUDPServer(
            (ip, port), self._create_dispatchers(signal_name_list))

    def _callback(self, osc_path, opt_params, *signal_data):
        try:
            signal_name = opt_params[0]
            self._signals[signal_name].push(signal_data)
        except Full:
            print("MuseOSCInputStream: queue is full")

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

    def read(self, signal_name: str, timeout=None) -> SignalData:
        return self._signals[signal_name].pop(timeout)

    def start(self):
        Thread(target=self._server.serve_forever).start()

    def shutdown(self):
        for _, signal in self._signals.items():
            signal.shutdown()
        self._server.shutdown()
        self._server.server_close()
