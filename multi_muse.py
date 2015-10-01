__author__ = 'benjamindeleener'

import sys
import time
from pymuse.ios import MuseServer
from pymuse.viz import MuseViewerSignal, MuseViewerConcentrationMellow
from pymuse.signals import MuseEEG, MuseConcentration, MuseMellow
from liblo import ServerError


def run_server(port=5001):
    # initialization of variables
    signals, viewers = dict(), dict()

    # EEG signal
    signal_eeg = MuseEEG(length=2000, acquisition_freq=220.0, do_fft=False)
    viewer_eeg = MuseViewerSignal(signal_eeg, 220.0, signal_boundaries=[600, 1200])

    signals['eeg'] = signal_eeg
    viewers['eeg'] = viewer_eeg

    # Initializing the server
    try:
        server = MuseServer(port=port, signal=signals, viewer=viewers)
    except ServerError, err:
        print str(err)
        sys.exit(1)

    # Displaying the viewers
    for sign in viewers:
        viewers[sign].show()

    return server


def main():
    server_5001 = run_server(5001)
    server_5002 = run_server(5002)

    # Starting the server
    try:
        server_5001.start()
        server_5002.start()
        while 1:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print "\nEnd of program: Caught KeyboardInterrupt"
        sys.exit(0)

if __name__ == "__main__":
    main()
