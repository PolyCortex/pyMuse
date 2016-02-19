__author__ = 'benjamindeleener'
from liblo import *
import socket


class MuseIOUDP():
    def __init__(self, port, signal=None, viewer=None):
        self.signal = signal
        self.viewer = viewer
        self.game = None
        self.port = port
        self.udp_ip = '127.0.0.1'

    def initializePort(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.udp_ip, self.port))
        print 'Port started to listen'
        while True:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            print data



class MuseServer(ServerThread):
    # listen for messages on port 5001
    def __init__(self, port, signal, viewer):
        self.signal = signal
        self.viewer = viewer
        self.game = None

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
    io_udp = MuseIOUDP(5000)
    io_udp.initializePort()
