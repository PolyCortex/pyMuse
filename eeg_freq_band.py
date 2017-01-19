__author__ = 'benjamindeleener'

import sys
import time
from pymuse.ios import OpenBCIIO, MuseIO, MuseIOError
from pymuse.signals import MultiChannelSignal
from pymuse.pipeline import Analyzer


def main():
    # initialization of variables
    signals, viewers = dict(), dict()

    # EEG signal
    signal_eeg = MultiChannelSignal(length=2000,
                                    estimated_acquisition_freq=250.0,
                                    label_channels=['central', 'right', 'left', 'top'])

    signals['eeg'] = signal_eeg

    # Initializing the analyzer
    """
    list_process=['ButterFilter',
                                      'WriteToFile',
                                      'FFT'],
                        list_params=[{'filter_type': 'bandpass', 'order': 1, 'cutoff_frequency': '0.25,35', 'acquisition_freq': 220.0},
                                     {'file_name': '/Users/benjamindeleener/data/test_muse/test.csv', 'save_delay': 180.0},
                                     None],

                                     {'filter_type': 'highpass', 'order': 1, 'cutoff_frequency': '0.5', 'acquisition_freq': 250.0},
    """
    pipeline = Analyzer(signal=signals['eeg'],
                        window_duration=1000,
                        analysis_frequency=20.0,
                        list_process=['ButterFilter',
                                      'ButterFilter',
                                      'ButterFilter',
                                      'FFT'],
                        list_params=[{'filter_type': 'bandstop', 'order': 3, 'cutoff_frequency': '40.0,80.0', 'acquisition_freq': 250.0},
                                     {'filter_type': 'lowpass', 'order': 2, 'cutoff_frequency': '35.0', 'acquisition_freq': 250.0},
                                     {'filter_type': 'highpass', 'order': 2, 'cutoff_frequency': '1.0', 'acquisition_freq': 250.0},
                                     None],
                        processes_to_visualize=[3])

    # Initializing the server
    try:
        #server = MuseIO(port=5001, signal=signals)
        #'/dev/tty.usbserial-DB00MF30'
        server = OpenBCIIO(port_name='COM3', baud=115200, signal=signals, index_channels=[0, 1, 2, 3])
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
