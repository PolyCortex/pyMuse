__author__ = 'Stephanie Dolbec'

import sys
import time
from pymuse.ios import OpenBCIIO, MuseIO, MuseIOError
from pymuse.signals import MultiChannelSignal
from pymuse.pipeline import Analyzer
import easygui


def main():
    # initialization of variables
    signals, viewers = dict(), dict()

    # EEG signal
    signal_eeg = MultiChannelSignal(length=2000,
                                    estimated_acquisition_freq=250.0,
                                    label_channels=['P7', 'PO7', 'O1', 'O2', 'PO8', 'P8'])

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

    path = '/Users/stephaniedolbec/Desktop'
    test_date = '20170419' # YYYYMMDD

    # TODO : write function
    msg = "Please fill in the fields below"
    title = "Intialization of data acquisition(" + test_date + ")"
    fieldNames = ["Initials", "Frequency (Hz)", "Test number"]
    fieldValues = easygui.multenterbox(msg, title, fieldNames)
    if fieldValues is None:
        exit(0)
    # make sure that none of the fields were left blank
    while 1:
        errmsg = ""
        for i, name in enumerate(fieldNames):
            if fieldValues[i].strip() == "":
                errmsg += "{} is a required field.\n\n".format(name)
        if errmsg == "":
            break  # no problems found
        fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
        if fieldValues is None:
            break
    name = format(fieldValues[0])
    freq = format(fieldValues[1])
    test_number = format(fieldValues[2])
    file_name = '/data_' + test_date + '_' + name + '_' + test_number + '_' + freq + 'Hz.csv'


    pipeline = Analyzer(signal=signals['eeg'],
                        window_duration=2500,
                        analysis_frequency=10.0,
                        list_process=['ButterFilter',
                                      'ButterFilter',
                                      'ButterFilter',
                                      'WriteToFile'],
                        list_params=[{'filter_type': 'bandstop', 'order': 3, 'cutoff_frequency': '40.0,80.0',
                                      'acquisition_freq': 250.0},
                                     {'filter_type': 'lowpass', 'order': 3, 'cutoff_frequency': '50.0',
                                      'acquisition_freq': 250.0},
                                     {'filter_type': 'highpass', 'order': 3, 'cutoff_frequency': '1.0',
                                      'acquisition_freq': 250.0},
                                     {'file_name': path + file_name, 'save_delay': 10.0}],
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
