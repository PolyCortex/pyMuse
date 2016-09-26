__author__ = 'benjamindeleener'

import sys
import time
from pymuse.ios import MuseIO, MuseIOError
from pymuse.viz import ViewerFrequencySpectrum
from pymuse.signals import MultiChannelSignal
from pymuse.pipeline import Analyzer

import numpy as np


def main():
    # initialization of variables
    signals, viewers = dict(), dict()

    # EEG signal
    signal_eeg = MultiChannelSignal(length=2000,
                                    estimated_acquisition_freq=220.0,
                                    label_channels=['Left ear', 'Left forehead', 'Right forehead', 'Right ear'])

    signals['eeg'] = signal_eeg

    # Initializing the analyzer
    pipeline = Analyzer(signal=signals['eeg'], window_duration=200, analysis_frequency=10.0, list_process=['FFT'])

    # Initializing the frequency spectrum viewer
    viewer_eeg = ViewerFrequencySpectrum(signal=pipeline.get_final_queue(),
                                         refresh_freq=15.0,
                                         signal_boundaries=[0, 20],
                                         label_channels=['Left ear', 'Left forehead', 'Right forehead', 'Right ear'])
    viewers['fft'] = viewer_eeg

    # Initializing the server
    try:
        server = MuseIO(port=5001, signal=signals)
    except MuseIOError, err:
        print str(err)
        sys.exit(1)

    pipeline.start()

    # Displaying the viewers
    for sign in viewers:
        viewers[sign].start()

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
