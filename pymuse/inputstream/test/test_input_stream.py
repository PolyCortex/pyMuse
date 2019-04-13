import random
import time
import unittest
from threading import Thread
from pythonosc import udp_client
from pymuse.signal import SignalData
from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream
from pymuse.inputstream.muse_constants import MUSE_ACQUISITION_FREQUENCIES, MUSE_OSC_PATH

SOUGHT_DATA_LIST: list = ['eeg', 'touching_forehead']
EEG_MESSAGES_LIST: list = [(0, 1, 2, 3), (50, 51, 52, 53),
                           (100, 101, 102, 103), (200, 201, 202, 203), (252, 253, 254, 255)]
TOUCHING_FOREHEAD_MESSAGES_LIST: list = [(0, ), (1, )]


class InputStreamTest(unittest.TestCase):
    def create_client(self, sought_data: str, sent_data: list) -> udp_client.SimpleUDPClient:
        client = udp_client.SimpleUDPClient('127.0.0.1', 5000)
        for data in sent_data:
            client.send_message(MUSE_OSC_PATH[sought_data], data)
            time.sleep(1 / MUSE_ACQUISITION_FREQUENCIES[sought_data])

    def read_messages(self, messages: list, signal_name: str):
        for index, message in enumerate(messages):
            time: int = index * (1 / MUSE_ACQUISITION_FREQUENCIES[signal_name])
            expected_signal_data: SignalData = SignalData(time, message)
            self.assertEqual(self.muse_input_stream.read(
                signal_name), expected_signal_data)

    def test_read(self):
        self.muse_input_stream: MuseOSCInputStream = MuseOSCInputStream(
            SOUGHT_DATA_LIST, '127.0.0.1', 5000)
        self.muse_input_stream.start()
        Thread(self.create_client(
            SOUGHT_DATA_LIST[0], EEG_MESSAGES_LIST)).start()
        Thread(self.create_client(
            SOUGHT_DATA_LIST[1], TOUCHING_FOREHEAD_MESSAGES_LIST)).start()
        self.read_messages(EEG_MESSAGES_LIST, SOUGHT_DATA_LIST[0])
        self.read_messages(TOUCHING_FOREHEAD_MESSAGES_LIST,
                           SOUGHT_DATA_LIST[1])
        self.muse_input_stream.shutdown()


if __name__ == '__main__':
    unittest.main()
