__author__ = 'benjamindeleener'
has_liblo = True
try:
    from liblo import *
except ImportError:
    has_liblo = False

has_oscserver = True
try:
    from OSC import OSCServer
except ImportError:
    has_oscserver = False

import types
from time import sleep


# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is
# set to False
def handle_timeout(self):
    self.timed_out = True


class MuseIOOSC():
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
        self.server.addMsgHandler("/muse/eeg", self.callback_eeg_raw)
        self.server.addMsgHandler("default", self.default_handler)

    def default_handler(self, addr, tags, stuff, source):
        # nothing to do here. This function is called for all messages that are not supported by the application.
        print "SERVER: No handler registered for ", addr
        return None

    def callback_eeg_raw(self, path, tags, args, source):
        # which user will be determined by path:
        # we just throw away all slashes and join together what's left
        user = ''.join(path.split("/"))
        # tags will contain 'ffff'
        # args is a OSCMessage with data
        # source is where the message came from (in case you need to reply)
        self.signal['eeg'].add_time()
        self.signal['eeg'].add_l_ear(args[0])
        self.signal['eeg'].add_l_forehead(args[1])
        self.signal['eeg'].add_r_forehead(args[2])
        self.signal['eeg'].add_r_ear(args[3])
        self.viewer['eeg'].refresh()
        #print args[0], args[1], args[2], args[3]

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


class MuseServer(ServerThread):
    # listen for messages on port 5001
    def __init__(self, port, signal, viewer):
        global has_liblo
        self.signal = signal
        self.viewer = viewer
        self.game = None
        self.server_initialized = False

        if has_liblo:
            self.server_initialized = True
            ServerThread.__init__(self, port)

    # receive accelrometer data
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):
        acc_x, acc_y, acc_z = args
        # print "%s %f %f %f" % (path, acc_x, acc_y, acc_z)

    # receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        if 'eeg' in self.signal:
            #print self.port, args
            self.signal['eeg'].add_time()
            self.signal['eeg'].add_l_ear(args[0])
            self.signal['eeg'].add_l_forehead(args[1])
            self.signal['eeg'].add_r_forehead(args[2])
            self.signal['eeg'].add_r_ear(args[3])
            self.viewer['eeg'].refresh()

    # receive alpha relative data
    @make_method('/muse/elements/alpha_relative', 'ffff')
    def alpha_callback(self, path, args):
        if 'alpha_rel' in self.signal:
            self.signal['alpha_rel'].add_time()
            self.signal['alpha_rel'].add_l_ear(args[0])
            self.signal['alpha_rel'].add_l_forehead(args[1])
            self.signal['alpha_rel'].add_r_forehead(args[2])
            self.signal['alpha_rel'].add_r_ear(args[3])
            self.viewer['alpha_rel'].refresh()

    # receive alpha relative data
    @make_method('/muse/elements/experimental/concentration', 'f')
    def concentration_callback(self, path, args):
        if 'concentration' in self.signal:
            self.signal['concentration'].add_time()
            self.signal['concentration'].add_concentration(args[0])
            self.viewer['concentration-mellow'].refresh()
            self.game.change_velocity(self.signal['concentration'].concentration)

    # receive mellow data - viewer is the same as concentration
    @make_method('/muse/elements/experimental/mellow', 'f')
    def mellow_callback(self, path, args):
        if 'mellow' in self.signal:
            self.signal['mellow'].add_time()
            self.signal['mellow'].add_mellow(args[0])
            self.viewer['concentration-mellow'].refresh()

    # handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        test = args
        # print "Unknown message \n\t Source: '%s' \n\t Address: '%s' \n\t Types: '%s ' \n\t Payload: '%s'" %
        # (src.url, path, types, args)


if __name__ == "__main__":
    io_udp = MuseIOOSC()
    io_udp.start()

