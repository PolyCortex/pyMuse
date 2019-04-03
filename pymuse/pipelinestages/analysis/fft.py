import numpy as np
import scipy.fftpack
from enum import Enum
from pymuse.pipelinestages.pipeline_stage import PipelineStage

DEFAULT_WINDOW_SIZE: int = 1024


class ScalingType(Enum):
    POWER_SPECTRAL_ESTIMATION = 'POWER_SPECTRAL_ESTIMATION',
    AMPLITUDE = 'AMPLITUDE'


class FFT(PipelineStage):
    """
    Pipeline stage that use Fast Fourier Transform to perform a Fourier transformation of your signal.
    It puts your data in a window object.
    """

    def __init__(self, window_size: int = DEFAULT_WINDOW_SIZE, detrending_method: str = None, scaling_type: ScalingType = ScalingType.AMPLITUDE):
        super().__init__()
        self._window_size = window_size
        self._buffer_window = None
        self._detrending_method = detrending_method
        if isinstance(scaling_type, ScalingType):
            self._scaling_type = scaling_type
        else:
            self._scaling_type = ScalingType.AMPLITUDE

    def _execute(self):
        self._fill_window()
        ###################
        import matplotlib.pyplot as plt
        plt.plot(self._buffer_window[0],'k')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.title('Frequency domain')
        plt.show()
        ##################
        if (self._detrending_method is not(None)):
            self._detrend()
        # TODO: Overlapping with Hamming Window and Square window and Welch's method
        freq_signals = self._transform_window_to_freq()
        self._write_queues_out(freq_signals)

    def _fill_window(self):
        data = self._queue_in.get()
        self._buffer_window = np.empty(
            (len(data.values), self._window_size))  # Allocate a buffer window
        self._add_data_to_buffer_window(0, data)
        # From 1 since we already consumed a data
        for i in range(1, len(self._buffer_window)):
            data = self._queue_in.get()
            self._add_data_to_buffer_window(i, data)

    def _add_data_to_buffer_window(self, index, data):
        for channelIndex in range(len(data.values)):
            self._buffer_window[index][channelIndex] = data.values[channelIndex]

    def _detrend(self):
        for i in len(self._buffer_window):
            self._buffer_window[i] = scipy.signal.detrend(
                self._buffer_window, type=self._detrending_method)

    def _transform_window_to_freq(self):
        freq_signals = []
        for buffer_window in self._buffer_window:
            freq_signal = self._fft(buffer_window)
            freq_signals.append(self._remove_imaginary_part(freq_signal))
        return freq_signals

    def _remove_imaginary_part(self, freq_signal):
        return freq_signal[0:(int)(np.floor(len(freq_signal)/2) + 1)]

    def _fft(self, window):
        if (self._scaling_type == ScalingType.AMPLITUDE):
            return 2*np.abs(scipy.fftpack.fft(window))/len(window)
        else:
            return np.abs(scipy.fftpack.fft(window) /
                          len(window)) ** 2
