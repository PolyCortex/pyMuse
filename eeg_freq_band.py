__author__ = 'benjamindeleener'

import sys
import time
from pymuse.ios import MuseIO, MuseIOError
from pymuse.signals import MultiChannelSignal
from pymuse.pipeline import Analyzer


def main():
    # initialization of variables
    signals, viewers = dict(), dict()

    # EEG signal
    signal_eeg = MultiChannelSignal(length=2000,
                                    estimated_acquisition_freq=220.0,
                                    label_channels=['Left ear', 'Left forehead', 'Right forehead', 'Right ear'])

    signals['eeg'] = signal_eeg

    # Initializing the analyzer
    pipeline = Analyzer(signal=signals['eeg'],
                        window_duration=1000,
                        analysis_frequency=24.0,
                        list_process=['FFT'],
                        processes_to_visualize=['FFT'])

    # Initializing the server
    try:
        server = MuseIO(port=5001, signal=signals)
    except MuseIOError, err:
        print str(err)
        sys.exit(1)

    pipeline.start()

    # Starting the server
    try:
        server.start()
        while 1:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print "\nEnd of program: Caught KeyboardInterrupt"
        sys.exit(0)

if __name__ == "__main__":
    main()
