from utils import Thread
from signals import MultiChannelFrequencySignal
import numpy as np
import time


class Process(Thread):
    def __init__(self, queue_in, queue_out):
        super(Process, self).__init__()
        self.name = 'process'

        self.queue_in = queue_in
        self.queue_out = queue_out
        self.data = None

    def process(self, data_in):
        return None

    def refresh(self):
        while True:
            data_in = self.queue_in.get()
            self.data = self.process(data_in)
            self.queue_in.task_done()

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


class Concentration(Process):
    def __init__(self, queue_in, queue_out):
        super(Concentration, self).__init__(queue_in, queue_out)
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
