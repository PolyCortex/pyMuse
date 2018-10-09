__author__ = 'benjamindeleener'

has_oscserver = True
try:
    from OSC import OSCServer, OSCError
except ImportError:
    has_oscserver = False

import types
import time
import timeit
import sys
from datetime import datetime, timedelta
from constants import DEFAULT_MUSEIO_IP, DEFAULT_MUSEIO_PORT, DEFAULT_FREQ, DEFAULT_UDPIO_IP, DEFAULT_UDPIO_PORT


# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is
# set to False
def handle_timeout(self):
    self.timed_out = True


class MuseIOError(OSCError):
    def __init__(self):
        super(MuseIOError, self).__init__()


class MuseIO():
    def __init__(self, port=DEFAULT_MUSEIO_PORT, signal=None, ip=DEFAULT_MUSEIO_IP):
        self.signal = signal
        self.port = port
        self.udp_ip = ip

        if not has_oscserver:
            raise Exception('ERROR: OSC not found')

        self.server = OSCServer((self.udp_ip, self.port))
        self.server.timeout = 0
        self.current_sample_id = 0

        # funny python's way to add a method to an instance of a class
        self.server.handle_timeout = types.MethodType(handle_timeout, self.server)

        # add message handlers
        if 'eeg' in self.signal:
            self.server.addMsgHandler('/muse/eeg', self.callback_eeg_raw)
        if 'concentration' in self.signal:
            self.server.addMsgHandler('/muse/elements/beta_relative/', self.callback_concentration)
        
    def callback_eeg_raw(self, path, tags, args, source):
        if 'eeg' in self.signal:
            self.signal['eeg'].lock.acquire()
            self.signal['eeg'].id = self.current_sample_id
            self.signal['eeg'].add_data(args, add_time=False)
            self.signal['eeg'].add_time(time.time())
            self.signal['eeg'].add_datetime(datetime.now())
            self.signal['eeg'].lock.release()

    def callback_concentration(self, path, tags, args, source):
        if 'concentration' in self.signal:
            self.signal['concentration'].lock.acquire()
            self.signal['concentration'].id = self.current_sample_id
            self.signal['concentration'].add_data(args, add_time=False)
            self.signal['concentration'].add_time(time.time())
            self.signal['concentration'].add_datetime(datetime.now())
            self.signal['concentration'].lock.release()

    def handle_request(self):
        self.server.timed_out = False
        # handle all pending requests then return
        while not self.server.timed_out:
            self.server.handle_request()

    def start(self, freq=DEFAULT_FREQ):
        update_timing = 1.0/float(freq)
        while True:
            try:
                time.sleep(update_timing)
                self.handle_request()
            except KeyboardInterrupt:
                print('KeyboardInterrupt on line {}'.format(sys.exc_info()[-1].tb_lineno))
                sys.exit(2)
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                print(str(e))
                sys.exit(2)


class UDPIO(object):
    def __init__(self, freq=DEFAULT_FREQ, udp_ip=DEFAULT_UDPIO_IP, udp_port=DEFAULT_UDPIO_PORT, index_channels=None, signal=None, channels=None):
        self.signal = signal

        self.udp_ip = udp_ip
        self.udp_port = udp_port

        self.channels = channels
        self.index_channels = index_channels
        if self.index_channels is None:
            self.index_channels = range(0, 4)

    def start(self):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.udp_ip, self.udp_port))
        while True:
            data, addr = sock.recvfrom(512)  # buffer size is 1024 bytes
            voltage_values = [float(d) for d in data.split(', ')]

            self.signal['eeg'].lock.acquire()
            self.signal['eeg'].add_data(voltage_values)
            self.signal['eeg'].lock.release()

class OpenBCIIO(object):
    def __init__(self, port_name=None, baud=115200, index_channels=None, signal=None, channels=None):
        import openbci.open_bci_v3 as bci

        self.signal = signal

        self.port_name = port_name
        self.baud = baud

        self.channels = channels
        self.index_channels = index_channels
        if self.index_channels is None:
            self.index_channels = range(0, 8)

        self.nb_samples_out = -1
        self.tick = timeit.default_timer()
        self.start_tick = self.tick

        self.board = bci.OpenBCIBoard(port=self.port_name, scaled_output=False, log=True, filter_data=True)
        print("Board Instantiated")
        self.board.ser.write('v')
        self.sample_rate = float(self.board.getSampleRate())
        print 'Sample Rate: ', self.sample_rate
        time.sleep(5)

        self.current_sample_id = 0
        self.init_sample_id = 0
        self.init_time = None  # datetime.now()

    def start(self):
        self.board.start_streaming(self.callback_rawdata)

    def callback_rawdata(self, sample):
        id = sample.id
        if self.init_time is None:
            self.init_sample_id = id
            self.init_time = datetime.now()

        data = sample.channel_data
        data_to_save = [data[ind] for ind in self.index_channels]
        self.signal['eeg'].lock.acquire()
        self.signal['eeg'].id = sample.id
        self.signal['eeg'].add_data(data_to_save, add_time=False)
        self.signal['eeg'].add_time((self.current_sample_id + sample.id) / self.sample_rate)
        self.signal['eeg'].add_datetime(self.init_time + timedelta(seconds=(self.current_sample_id + sample.id - self.init_sample_id) / self.sample_rate))
        self.signal['eeg'].lock.release()
        if sample.id == 255:
            self.current_sample_id += 256

    def printData(self, sample):
        print "----------------"
        print("%f" % (sample.id))
        print sample.channel_data
        print sample.aux_data
        print "----------------"

        new_tick = timeit.default_timer()
        elapsed_time = new_tick - self.tick
        current_samples_out = self.nb_samples_out
        print "--- at t: ", (new_tick - self.start_tick), " ---"
        print "elapsed_time: ", elapsed_time
        print "nb_samples_out: ", current_samples_out - self.nb_samples_out
        sampling_rate = (current_samples_out - self.nb_samples_out) / elapsed_time
        print "sampling rate: ", sampling_rate
        self.tick = new_tick

if __name__ == "__main__":
    io_udp = MuseIO()
    io_udp.start()

