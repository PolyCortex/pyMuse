import numpy as np
import scipy
from pymuse.pipelinestages.pipeline_stage import PipelineStage

DEFAULT_WINDOW_SIZE: int = 1024


class FFT(PipelineStage):
    """
    Pipeline stage that use Fast Fourier Transform to perform a Fourier transformation of your signal.
    It puts your data in a window object.
    """

    def __init__(self, window_size: int = DEFAULT_WINDOW_SIZE, detrending_method: str = None):
        super().__init__()
        self.buffer_window = np.empty(window_size)
        self.detrending_method = detrending_method

    def _execute(self):
        self._fill_window()
        if (self.detrending_method is not(None)):
            self._detrend()
        # Overlapping with Hamming Window and Square window and Welch's method
        # Do FFT (Absolute or power)
        power = np.abs(scipy.fftpack.fft(self.buffer_window) /
               len(self.buffer_window)) ** 2
        # Write FFT product to queues_out

    def _initialization_hook(self):
        pass

    def _shutdown_hook(self):
        pass

    def _fill_window(self):
        for i in len(self.buffer_window):
            self.buffer_window[i] = self._queue_in.get()

    def _detrend(self):
        self.buffer_window = scipy.signal.detrend(self.buffer_window, type = self.detrending_method)
