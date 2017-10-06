from utils import Thread
from signals import MultiChannelFrequencySignal
import numpy as np
from scipy import signal
import time
from datetime import datetime
from pipeline import InterfaceEvents


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
            try:
                data_in = self.queue_in.get()
                time_now = datetime.now()
                self.data = self.process(data_in)
                self.queue_in.task_done()
                self.duration_process = (datetime.now() - time_now).total_seconds()
                if self.duration_process == 0.0:
                    freq = 0.0
                else:
                    freq = 1.0 / self.duration_process
                #print 'Frequency process (' + self.name + ') = ' + str(round(freq, 2))
                # because we want that the speed of the pipeline is the same as the speed of the slowest process, we need to
                # wait for the next process to finish before adding a new item in the queue
                self.queue_out.put(self.data, block=True, timeout=None)
                time.sleep(0.001)
            except KeyboardInterrupt:
                import sys
                print('KeyboardInterrupt on line {}'.format(sys.exc_info()[-1].tb_lineno))
                sys.exit(2)
            except Exception as e:
                import sys
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                print(str(e))
                sys.exit(2)


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
    def __init__(self, queue_in, queue_out, param):
        super(ButterFilter, self).__init__(queue_in, queue_out)
        self.name = 'butterfilter'
        if 'filter_type' in param:
            self.filter_type = str(param['filter_type'])
        else:
            self.filter_type = 'low'
        if 'order' in param:
            self.order = int(param['order'])
        else:
            self.order = 1
        if 'cutoff_frequency' in param:
            self.cutoff_frequency = [np.float(f) for f in param['cutoff_frequency'].split(',')]  # not normalized
        else:
            self.cutoff_frequency = [35.0]
        if 'acquisition_freq' in param:
            self.acquisition_freq = float(param['acquisition_freq'])
        else:
            self.acquisition_freq = 220.0

        if self.filter_type in ['lowpass', 'highpass']:
            self.filter_param = self.getcoeffshigh(self.cutoff_frequency[0], self.acquisition_freq, self.order, self.filter_type)
        elif self.filter_type in ['bandpass', 'bandstop']:
            self.filter_param = self.getcoeffsband(self.cutoff_frequency[0], self.cutoff_frequency[1], self.acquisition_freq, self.order, self.filter_type)

    def getcoeffshigh(self, fcut, fs, order=1, filter_type='lowpass'):
        fnyq = 0.5 * fs  # Get the Nyquist frequency from sampling frequency
        fr = fcut / fnyq  # Normalize cutoff frequency by the Nyquist frequency
        b, a = signal.butter(order, fr, btype=filter_type)  # Get the filter coefficients
        return b, a

    def getcoeffsband(self, lowfcut, highfcut, fs, order=1, filter_type='bandpass'):
        fnyq = 0.5 * fs
        low = lowfcut / fnyq
        high = highfcut / fnyq
        b, a = signal.butter(order, [low, high], btype=filter_type)
        return b, a

    def process(self, data_in):
        # print data_in.data.shape[1]  # len of data vector in channel
        #data_in.data = signal.filtfilt(self.filter_param[0], self.filter_param[1], data_in.data, method='gust')
        data_in.data = signal.filtfilt(self.filter_param[0], self.filter_param[1], data_in.data, method='pad', padtype='even')
        return data_in


class AssociateEvent(Process):
    def __init__(self, queue_in, queue_out, param):
        super(AssociateEvent, self).__init__(queue_in, queue_out)
        self.name = 'associate_event'
        self.events_interface = InterfaceEvents()

    def start(self):
        self.events_interface.start()
        super(AssociateEvent, self).start()

    def process(self, data_in):
        data_in.event_related = self.events_interface.find_closest_event(data_in.datetimes[0])
        return data_in


class WriteToFile(Process):
    def __init__(self, queue_in, queue_out, param):
        super(WriteToFile, self).__init__(queue_in, queue_out)
        self.name = 'writetofile'
        self.last_save = datetime.now()
        self.data_to_write = []
        self.time_to_write = []
        if 'file_name' in param:
            self.file_name = str(param['file_name'])
        else:
            self.file_name = 'dataAcquisition.csv'
        if 'save_delay' in param:
            self.save_delay = param['save_delay']
        else :
            self.save_delay = 180.0

    def process(self, data_in):
        time_now = datetime.now()
        seconds_passed = (time_now - self.last_save).total_seconds()
        if seconds_passed > self.save_delay:
            self.data_to_write.append(data_in.data)
            self.time_to_write.append(data_in.datetimes[0])

            f_handle = open(self.file_name, 'a')
            for i, line in enumerate(self.data_to_write):
                strheader = str(self.time_to_write[i]) + ', Channels: ' + str(data_in.number_of_channels) + ', ' + ', '.join(data_in.label_channels) + ', event, ' + data_in.related_event
                np.savetxt(f_handle, line, header=strheader, newline='\n', delimiter=',')
            f_handle.close()
            self.last_save = datetime.now()

            self.data_to_write = []
            self.time_to_write = []
        else:
            self.data_to_write.append(data_in.data)
            self.time_to_write.append(data_in.datetimes[0])

        return data_in
