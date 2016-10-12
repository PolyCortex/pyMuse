__author__ = 'benjamindeleener'

has_oscserver = True
try:
    from OSC import OSCServer, OSCError
except ImportError:
    has_oscserver = False

import types
import time
import timeit


# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is
# set to False
def handle_timeout(self):
    self.timed_out = True


class MuseIOError(OSCError):
    def __init__(self):
        super(MuseIOError, self).__init__()


class MuseIO():
    def __init__(self, port=5001, signal=None):
        self.signal = signal
        self.port = port
        self.udp_ip = '127.0.0.1'

        if not has_oscserver:
            raise Exception('ERROR: OSC not found')

        self.server = OSCServer((self.udp_ip, self.port))
        self.server.timeout = 0

        # funny python's way to add a method to an instance of a class
        self.server.handle_timeout = types.MethodType(handle_timeout, self.server)

        # add message handlers
        if 'eeg' in self.signal:
            self.server.addMsgHandler('/muse/eeg', self.callback_eeg_raw)
        if 'concentration' in self.signal:
            self.server.addMsgHandler('/muse/elements/experimental/concentration', self.callback_concentration)
        if 'mellow' in self.signal:
            self.server.addMsgHandler('/muse/elements/experimental/mellow', self.callback_mellow)
        self.server.addMsgHandler("default", self.default_handler)

    def default_handler(self, addr, tags, stuff, source):
        # nothing to do here. This function is called for all messages that are not supported by the application.
        #print "SERVER: No handler registered for ", addr
        return None

    def callback_eeg_raw(self, path, tags, args, source):
        # which user will be determined by path:
        # we just throw away all slashes and join together what's left
        # tags will contain 'ffff'
        # args is a OSCMessage with data
        # source is where the message came from (in case you need to reply)
        self.signal['eeg'].lock.acquire()
        self.signal['eeg'].add_data(args)
        self.signal['eeg'].lock.release()

    def callback_concentration(self, path, tags, args, source):
        if 'concentration' in self.signal:
            self.signal['concentration'].add_time()
            self.signal['concentration'].add_concentration(args[0])
            #self.game.change_velocity(self.signal['concentration'].concentration)

    def callback_mellow(self, path, tags, args, source):
        if 'mellow' in self.signal:
            self.signal['mellow'].add_time()
            self.signal['mellow'].add_mellow(args[0])

    def handle_request(self):
        # clear timed_out flag
        self.server.timed_out = False
        # handle all pending requests then return
        while not self.server.timed_out:
            self.server.handle_request()

    def start(self, freq=220):
        update_timing = 1.0/float(freq)
        while True:
            time.sleep(update_timing)
            self.handle_request()


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
        print 'Sample Rate: ', self.board.getSampleRate()
        time.sleep(5)

    def start(self):
        self.board.start_streaming(self.callback_rawdata)

    def callback_rawdata(self, sample):
        data = sample.channel_data
        data_to_save = [data[ind] for ind in self.index_channels]
        self.signal['eeg'].lock.acquire()
        self.signal['eeg'].add_data(data_to_save)
        self.signal['eeg'].lock.release()

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

