import numpy as np
import scipy
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
        self.buffer_window = np.empty(window_size)
        self.detrending_method = detrending_method
        if isinstance(scaling_type, ScalingType):
            self.scaling_type = scaling_type
        else:
            self.scaling_type = ScalingType.AMPLITUDE

    def _execute(self):
        self._fill_window()
        if (self.detrending_method is not(None)):
            self._detrend()

        # Overlapping with Hamming Window and Square window and Welch's method

        self._write_queues_out(self._fft())

    def _fill_window(self):
        for i in len(self.buffer_window):
            self.buffer_window[i] = self._queue_in.get()

    def _detrend(self):
        self.buffer_window = scipy.signal.detrend(
            self.buffer_window, type=self.detrending_method)

    def _fft(self):
        if (self.scaling_type == ScalingType.AMPLITUDE):
            return 2*np.abs(scipy.fftpack.fft(self.buffer_window))/len(self.buffer_window)
        else:
            return np.abs(scipy.fftpack.fft(self.buffer_window) /
                          len(self.buffer_window)) ** 2

