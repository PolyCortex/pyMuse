from utils import Thread
from signals import MultiChannelFrequencySignal
import numpy as np
import scipy.signal as sig
import time
from datetime import datetime


class Process(Thread):
    def __init__(self, queue_in, queue_out):
        super(Process, self).__init__()
        self.name = 'process'

        self.queue_in = queue_in
        self.queue_out = queue_out
        self.data = None

        self.duration_process = 0.0  # in seconds

    def process(self, data_in):
        return None

    def refresh(self):
        while True:
            data_in = self.queue_in.get()
            time_now = datetime.now()
            self.data = self.process(data_in)
            self.queue_in.task_done()
            self.duration_process = (datetime.now() - time_now).total_seconds()
            freq = 1.0 / self.duration_process
            #print 'Frequency process (' + self.name + ') = ' + str(round(freq, 2))

            # because we want that the speed of the pipeline is the same as the speed of the slowest process, we need to
            # wait for the next process to finish before adding a new item in the queue
            self.queue_out.put(self.data, block=True, timeout=None)
            time.sleep(0.001)


class FFT(Process):
    def __init__(self, queue_in, queue_out):
        super(FFT, self).__init__(queue_in, queue_out)
        self.name = 'fft'

    def process(self, data_in):
        k = np.arange(data_in.length)
        T = data_in.length / data_in.estimated_acquisition_freq
        frq = k / T  # two sides frequency range
        x_frq = frq[range(data_in.length / 2)]  # one side frequency range

        data_out_fft = np.fft.fft(data_in.data) / data_in.length  # fft computing and normalization
        data_out_fft = data_out_fft[:, range(data_in.length / 2)]

        data_out = MultiChannelFrequencySignal(length=data_in.length,
                                               estimated_acquisition_freq=data_in.estimated_acquisition_freq,
                                               number_of_channels=data_in.number_of_channels,
                                               label_channels=data_in.label_channels,
                                               data=data_out_fft,
                                               freq=x_frq)
        return data_out

class ButterFilter(Process):
    def __init__(self, queue_in, queue_out):
        super(ButterFilter, self).__init__(queue_in, queue_out)
        self.name = 'butterfilter'

    def getcoeffshigh(self, fcut, fs, order=5):
        fnyq = fs / 2 # Get the Nyquist frequency from sampling frequency
        high = fcut / fnyq # Normalize cutoff frequency by the Nyquist frequency
        [b, a] = sig.butter(order, high, btype='high') # Get the filter coefficients
        return b, a

    def getcoeffslow(self, fcut, fs, order=5):
        fnyq = fs / 2
        low = fcut / fnyq
        [b, a] = sig.butter(order, low, btype='low')
        return b, a

    def getcoeffsband(self, lowfcut, highfcut, fs, order=5):
        fnyq = fs / 2
        low = lowfcut / fnyq
        high = highfcut / fnyq
        [b, a] = sig.butter(order, [low, high], btype='band')
        return b, a

    def process(self, data_in, filterType, cutFrq, order=5):
        k = np.arange(data_in.length)
        fs = data_in.estimated_acquisition_freq
        T = data_in.length / fs
        frq = k / T
        x_frq = frq[range(data_in.length / 2)]

        if filterType=='high':
            [b, a] = self.getcoeffshigh(cutFrq,fs,order)
        elif filterType=='low':
            [b, a] = self.getcoeffslow(cutFrq,fs,order)
        else:
            [b, a] = self.getcoeffsband(cutFrq,fs,order)

        data_out_filter = sig.lfilter(b, a, data_in.data)

        data_out = MultiChannelFrequencySignal(length=data_in.length,
                                               estimated_acquisition_freq=data_in.estimated_acquisition_freq,
                                               number_of_channels=data_in.number_of_channels,
                                               label_channels=data_in.label_channels,
                                               data=data_out_filter,
                                               freq=x_frq)
        return data_out



