from pymuse.pipeline import Pipeline
from pymuse.configureshutdown import configure_shutdown
from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream
from pymuse.pipelinestages.analysis.fft import FFT
from time import sleep
import numpy as np
import matplotlib.pyplot as plt


fft = FFT()
muse_input_stream = MuseOSCInputStream()
pipeline = Pipeline(muse_input_stream.get_signal('eeg'), fft)
configure_shutdown(muse_input_stream, pipeline)
muse_input_stream.start()
pipeline.start()

while True:
    sleep(100)
    # signalAmp = pipeline.read_output_queue()
    # print('Signal AMP: ')
    # # print(signalAmp[0])
    # hz = np.linspace(0,256/2,len(signalAmp[0]))
    # plt.stem(hz,signalAmp[0],'k')
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Amplitude')
    # plt.title('Frequency domain')
    # plt.show()
