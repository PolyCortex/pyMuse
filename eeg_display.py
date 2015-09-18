__author__ = 'benjamindeleener'

import sys
import time
from pymuse.ios import MuseServer
from pymuse.viz import MuseViewerSignal, MuseViewerConcentrationMellow
from pymuse.signal import MuseSignal, MuseConcentration, MuseMellow
from liblo import ServerError


def main():
    signal, viewer = dict(), dict()

    signal_eeg = MuseSignal(length=2000, do_fft=False)
    viewer_eeg = MuseViewerSignal(signal_eeg, signal_boundaries=[600, 1200])

    signal['eeg'] = signal_eeg
    viewer['eeg'] = viewer_eeg

    signal_concentration = MuseConcentration(length=400)
    signal_mellow = MuseMellow(length=400)
    viewer_concentration_mellow = MuseViewerConcentrationMellow(signal_concentration, signal_mellow, signal_boundaries=[-0.1, 1.1])

    signal['concentration'] = signal_concentration
    signal['mellow'] = signal_mellow
    viewer['concentration-mellow'] = viewer_concentration_mellow

    try:
        server = MuseServer(signal=signal, viewer=viewer)
    except ServerError, err:
        print str(err)
        sys.exit(1)

    for signal in viewer:
        viewer[signal].show()

    server.start()
    while 1:
        time.sleep(0.01)

if __name__ == "__main__":
    main()
