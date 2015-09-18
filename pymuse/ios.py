__author__ = 'benjamindeleener'
from liblo import *


class MuseServer(ServerThread):
    # listen for messages on port 5001
    def __init__(self, signal, viewer):
        self.signal = signal
        self.viewer = viewer

        ServerThread.__init__(self, 5001)

    # receive accelrometer data
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):
        acc_x, acc_y, acc_z = args
        # print "%s %f %f %f" % (path, acc_x, acc_y, acc_z)

    # receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        self.signal.add_l_ear(args[0])
        self.signal.add_l_forehead(args[1])
        self.signal.add_r_forehead(args[2])
        self.signal.add_r_ear(args[3])
        print args

        self.viewer.refresh()

    # handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        test = args
        # print "Unknown message \n\t Source: '%s' \n\t Address: '%s' \n\t Types: '%s ' \n\t Payload: '%s'" %
        # (src.url, path, types, args)
