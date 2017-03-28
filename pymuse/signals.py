__author__ = 'benjamindeleener'
import numpy as np
from datetime import datetime, timedelta
import multiprocessing


def find_closest(A, target):
    # A must be sorted and must be a numpy array
    idx = A.searchsorted(target)
    idx = np.clip(idx, 1, len(A)-1)
    left = A[idx-1]
    right = A[idx]
    idx -= target - left < right - target
    return idx


class Signal(object):
    def __init__(self, length, estimated_acquisition_freq):
        self.id = 0
        self.length = length
        self.estimated_acquisition_freq = estimated_acquisition_freq
        self.time = np.linspace(-float(self.length) / self.estimated_acquisition_freq + 1.0 / self.estimated_acquisition_freq, 0.0, self.length)
        self.datetimes = np.array([datetime.now()]*self.length)
        self.init_time = datetime.now()
        self.lock = multiprocessing.Lock()

        self.related_event = '0'

    def add_time(self, diff=None):
        if diff is None:
            diff = datetime.now() - self.init_time
            diff = diff.total_seconds()
        self.time = np.roll(self.time, -1)
        self.time[-1] = float(diff * 1000.0)  # in milliseconds

    def add_datetime(self, value):
        self.datetimes = np.roll(self.datetimes, -1)
        self.datetimes[-1] = value

    def compute_real_acquisition_frequency(self, window=None):
        if not window or window > self.length:
            window = self.length

        diff_time = np.zeros(window)
        for k in range(0, window - 1):  # self.length, self.length - window, -1):
            diff_time[k] = self.time[self.length - k] - self.time[self.length - (k + 1)]
        acquisition_frequency = 1.0 / np.mean(diff_time)
        return acquisition_frequency


class MultiChannelSignal(Signal):
    def __init__(self, length=1000, estimated_acquisition_freq=220.0, number_of_channels=None, label_channels=None, signal_data=None, signal_time=None, datetimes=None):
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

        if signal_data is None:
            self.data = np.zeros((self.number_of_channels, self.length))
        else:
            self.data = signal_data

        if signal_time is not None:
            self.time = signal_time

        if datetimes is not None:
            self.datetimes = datetimes

    def add_data(self, s, add_time=True):
        """
        Function for adding a new element in the ndarray. This function calls the inherited function add_time.
        :param s: list of number, length of list must be equal to the number of channels
        :return: nothing
        """
        if len(s) == self.number_of_channels:
            if add_time:
                self.add_time()
            self.data = np.roll(self.data, -1, axis=1)
            self.data[:, -1] = s
        else:
            print 'Error: length of signal (=' + str(len(s)) + ') is not equal to the number of channel (=' + str(self.number_of_channels) + ').'

    def get_window_ms(self, length_window=200.0, time_start=None):
        """
        This function extracts a window from the signal with the specified length (in milliseconds).
        The effective length of the window (i.e., the number of elements) may vary, because the acquisition frequency varies.
        To get a window with a fixed number of elements, the simplest way to do it is to call: mysignal.signal[length_window:, :]
        :param length_window: length of the window to extract, in milliseconds
        :return: ndarray with the signal window
        """

        if time_start is None:
            # get number of elements to extract
            time_limit = self.datetimes[-1] - timedelta(milliseconds=length_window)
        else:
            time_limit = time_start

        length = self.estimated_acquisition_freq * length_window / 1000.0

        idx = np.searchsorted(self.datetimes, time_limit, side="left")

        # extract elements and return
        index_end = idx + length
        if index_end >= len(self.datetimes):
            index_end = len(self.datetimes)

        index_end = int(index_end)

        return self.time[idx:index_end], self.data[:, idx:index_end], self.datetimes[idx:index_end]

    def get_signal_window(self, length_window=200.0, time_start=None):
        signal_time, signal_data, signal_datetimes = self.get_window_ms(length_window=length_window, time_start=time_start)
        signal = MultiChannelSignal(length=len(signal_time), estimated_acquisition_freq=self.estimated_acquisition_freq,
                                    number_of_channels=self.number_of_channels, label_channels=self.label_channels,
                                    signal_data=signal_data, signal_time=signal_time, datetimes=signal_datetimes)
        return signal


class MultiChannelFrequencySignal:
    def __init__(self, length=1000, estimated_acquisition_freq=220.0, number_of_channels=None, label_channels=None, data=None, freq=None):
        self.length = length
        self.lock = multiprocessing.Lock()
        self.estimated_acq_freq = estimated_acquisition_freq
        self.label_channels = label_channels
        if number_of_channels:
            self.number_of_channels = number_of_channels
        else:
            if label_channels:
                self.number_of_channels = len(self.label_channels)
            else:
                self.number_of_channels = 1
                self.label_channels = ['']

        if data is None:
            self.data = np.zeros((self.number_of_channels, self.length))
        else:
            self.data = data

        if freq is None:
            self.freq = np.linspace(0, self.estimated_acq_freq, self.length / 2)
        else:
            self.freq = freq

    def set_data(self, data):
        self.data = data

    def set_freq(self, freq):
        self.freq = freq

    def get_frequency_power(self, freq_start, freq_end):
        freq = np.array(self.freq)
        idx_boundary = find_closest(freq, np.array([freq_start, freq_end]))
        power = np.zeros(self.number_of_channels)
        for i in range(self.number_of_channels):
            target_values = np.abs(self.data[i, idx_boundary[0]:idx_boundary[1]])**2
            power[i] = np.sum(target_values) / abs((freq[idx_boundary[1]] - freq[idx_boundary[0]]))
        return power

    def get_band_power(self, band='alpha', average=True):
        band_frequencies = {'delta': [1.0, 4.0],
                            'theta': [4.0, 8.0],
                            'alpha': [8.0, 13.0],
                            'alpha1': [8.0, 10.0],
                            'alpha2': [10.0, 13.0],
                            'beta': [13.0, 30.0],
                            'beta1': [13.0, 18.0],
                            'beta2': [18.0, 30.0],
                            'gamma': [30.0, 50.0],
                            'gamma1': [30.0, 41.0],
                            'gamma2': [41.0, 50.0]}

        band_powers = self.get_frequency_power(band_frequencies[band][0], band_frequencies[band][1])
        if average:
            return np.mean(band_powers)
        else:
            return band_powers



