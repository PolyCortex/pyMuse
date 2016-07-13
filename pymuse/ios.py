__author__ = 'benjamindeleener'

has_oscserver = True
try:
    from OSC import OSCServer, OSCError
except ImportError:
    has_oscserver = False
    raise Exception

import types
from time import sleep


# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is
# set to False
def handle_timeout(self):
    self.timed_out = True


class MuseIOError(OSCError):
    def __init__(self):
        super(MuseIOError, self).__init__()


class MuseIO():
    def __init__(self, port=5001, signal=None, viewer=None):
        self.signal = signal
        self.viewer = viewer
        self.game = None
        self.port = port
        self.udp_ip = '127.0.0.1'

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
        print "SERVER: No handler registered for ", addr
        return None

    def callback_eeg_raw(self, path, tags, args, source):
        # which user will be determined by path:
        # we just throw away all slashes and join together what's left
        # tags will contain 'ffff'
        # args is a OSCMessage with data
        # source is where the message came from (in case you need to reply)
        self.signal['eeg'].add_time()
        self.signal['eeg'].add_l_ear(args[0])
        self.signal['eeg'].add_l_forehead(args[1])
        self.signal['eeg'].add_r_forehead(args[2])
        self.signal['eeg'].add_r_ear(args[3])
        if 'eeg' in self.viewer:
            self.viewer['eeg'].refresh()
        #print args[0], args[1], args[2], args[3]

    def callback_concentration(self, path, tags, args, source):
        if 'concentration' in self.signal:
            self.signal['concentration'].add_time()
            self.signal['concentration'].add_concentration(args[0])
            self.viewer['concentration-mellow'].refresh()
            #self.game.change_velocity(self.signal['concentration'].concentration)

    def callback_mellow(self, path, tags, args, source):
        if 'mellow' in self.signal:
            self.signal['mellow'].add_time()
            self.signal['mellow'].add_mellow(args[0])
            self.viewer['concentration-mellow'].refresh()

    def handle_request(self):
        # clear timed_out flag
        self.server.timed_out = False
        # handle all pending requests then return
        while not self.server.timed_out:
            self.server.handle_request()

    def start(self, freq=220):
        update_timing = 1.0/float(freq)
        while True:
            sleep(update_timing)
            self.handle_request()


if __name__ == "__main__":
    io_udp = MuseIO()
    io_udp.start()

