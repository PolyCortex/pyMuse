import random
import time
import unittest
import unittest.mock
from pythonosc import udp_client
from signal import SignalData
from input_stream import MuseInputStream
from muse_constants import MUSE_EEG_ACQUISITION_FREQUENCY

MESSAGES_NUMBER = 16
MUSE_ACQUISITION_PERIOD = 1 / MUSE_EEG_ACQUISITION_FREQUENCY

class InputStreamTest(unittest.TestCase):
    def create_random_list(self):
        return random.sample(range(255), MESSAGES_NUMBER) 

    def create_client(self, sent_data: list):
        client = udp_client.SimpleUDPClient('127.0.0.1', 5001)
        for data in sent_data:
            client.send_message("/eeg", data)
            time.sleep(MUSE_ACQUISITION_PERIOD)

    def test_pop(self):
        random_bytes = self.create_random_list()
        sought_data_list = ['eeg']
        muse_input_stream = MuseInputStream(sought_data_list, '127.0.0.1', 5001)
        self.create_client(random_bytes)
        for i in range(MESSAGES_NUMBER):
            self.assertEqual(muse_input_stream.pop('eeg'), SignalData(i * MUSE_ACQUISITION_PERIOD, random_bytes[i]))
        muse_input_stream.close()

if __name__ == '__main__':
    unittest.main()
