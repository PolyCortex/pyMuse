__author__ = 'benjamindeleener'
import numpy as np
from datetime import datetime
import multiprocessing

class Signal(object):
    def __init__(self, length, estimated_acquisition_freq):
        self.length = length
        self.estimated_acq_freq = estimated_acquisition_freq
        self.time = np.linspace(-float(self.length) / self.estimated_acq_freq + 1.0 / self.estimated_acq_freq, 0.0, self.length)
        self.init_time = datetime.now()
        self.lock = multiprocessing.Lock()

    def add_time(self):
        diff = datetime.now() - self.init_time
        self.time = np.roll(self.time, -1)
        self.time[-1] = float(diff.total_seconds() * 1000)  # in milliseconds

    def compute_real_acquisition_frequency(self, window=None):
        if not window or window > self.length:
            window = self.length

        diff_time = np.zeros(window)
        for k in range(0, window - 1):  # self.length, self.length - window, -1):
            diff_time[k] = self.time[self.length - k] - self.time[self.length - (k + 1)]
        acquisition_frequency = 1.0 / np.mean(diff_time)
        return acquisition_frequency


class MultiChannelSignal(Signal):
    def __init__(self, length=1000, estimated_acquisition_freq=220.0, number_of_channels=None, label_channels=None):
        super(MultiChannelSignal, self).__init__(length, estimated_acquisition_freq)
        self.label_channels = label_channels
        if number_of_channels:
            self.number_of_channels = number_of_channels
        else:
            if label_channels:
                self.number_of_channels = len(self.label_channels)
            else:
                self.number_of_channels = 1
                self.label_channels = ['']
        self.data = np.zeros((self.number_of_channels, self.length))

    def add_data(self, s):
        """
        Function for adding a new element in the ndarray. This function calls the inherited function add_time.
        :param s: list of number, length of list must be equal to the number of channels
        :return: nothing
        """
        if len(s) == self.number_of_channels:
            self.add_time()
            self.data = np.roll(self.data, -1, axis=1)
            self.data[:, -1] = s
        else:
            print 'Error: length of signal (=' + str(len(s)) + ') is not equal to the number of channel (=' + str(self.number_of_channels) + ').'

    def get_window_ms(self, length_window=200.0):
        """
        This function extracts a window from the signal with the specified length (in milliseconds).
        The effective length of the window (i.e., the number of elements) may vary, because the acquisition frequency varies.
        To get a window with a fixed number of elements, the simplest way to do it is to call: mysignal.signal[length_window:, :]
        :param length_window: length of the window to extract, in milliseconds
        :return: ndarray with the signal window
        """
        # get number of elements to extract
        time_limit = self.time[-1] - length_window
        idx = np.searchsorted(self.time, time_limit, side="left")

        # extract elements and return
        return self.time[idx:], self.data[:, idx:]


class MuseEEG(Signal):
    def __init__(self, length=1000, acquisition_freq=220.0):
        super(MuseEEG, self).__init__(length, acquisition_freq)
        self.l_ear, self.l_forehead, self.r_forehead, self.r_ear = [0.0] * self.length, [0.0] * self.length, \
                                                                   [0.0] * self.length, [0.0] * self.length

    def add_l_ear(self, s):
        self.l_ear.append(s)
        del self.l_ear[0]

    def add_l_forehead(self, s):
        self.l_forehead.append(s)
        del self.l_forehead[0]

    def add_r_forehead(self, s):
        self.r_forehead.append(s)
        del self.r_forehead[0]

    def add_r_ear(self, s):
        self.r_ear.append(s)
        del self.r_ear[0]


class MuseConcentration(Signal):
    def __init__(self, length=200, acquisition_freq=10.0):
        super(MuseConcentration, self).__init__(length, acquisition_freq)
        self.concentration = [0.0] * self.length

    def add_concentration(self, s):
        self.concentration.append(s)
        del self.concentration[0]


class MuseMellow(Signal):
    def __init__(self, length=200, acquisition_freq=10.0):
        super(MuseMellow, self).__init__(length, acquisition_freq)
        self.mellow = [0.0] * self.length

    def add_mellow(self, s):
        self.mellow.append(s)
        del self.mellow[0]
