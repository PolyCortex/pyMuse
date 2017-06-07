__author__ = 'Benjamin De Leener'

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
                                    label_channels=['P7', 'PO7', 'O1', 'O2', 'PO8', 'P8'])

    signals['eeg'] = signal_eeg

    # Initializing the analyzer
    pipeline = Analyzer(signal=signals['eeg'],
                        window_duration=2000,
                        analysis_frequency=5.0,
                        list_process=['ButterFilter',
                                      'ButterFilter',
                                      'AssociateEvent',
                                      'WriteToFile'],
                        list_params=[{'filter_type': 'bandstop', 'order': 3, 'cutoff_frequency': '40.0,80.0',
                                      'acquisition_freq': 250.0},
                                     {'filter_type': 'highpass', 'order': 3, 'cutoff_frequency': '1.0',
                                      'acquisition_freq': 250.0},
                                     {'none': 'none'},
                                     {'file_name': '/Users/stephaniedolbec/data/test_ttih/acquisitions/'
                                                   'no_contact/20170327/data_7.csv', 'save_delay': 10.0}],
                        processes_to_visualize=[])

    # Initializing the server
    try:
        #server = MuseIO(port=5001, signal=signals)
        #'/dev/tty.usbserial-DB00MF30'
        server = OpenBCIIO(port_name='/dev/tty.usbserial-DB00MHSH', baud=115200, signal=signals, index_channels=[0, 1, 2, 3, 4, 5])
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
