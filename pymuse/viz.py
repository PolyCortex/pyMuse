__author__ = 'benjamindeleener'
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
import numpy as np
from utils import AutoQueue


def timeTicks(x, pos):
    d = timedelta(milliseconds=x)
    return str(d)


class Viewer(object):
    def __init__(self, refresh_freq=10.0, signal_boundaries=None):
        super(Viewer, self).__init__()
        self.name = 'viewer'

        self.refresh_freq = refresh_freq
        self.init_time = datetime.now()
        self.last_refresh = datetime.now()

        if signal_boundaries is not None:
            self.low, self.high = signal_boundaries[0], signal_boundaries[1]
        else:
            self.low, self.high = 0, 1

    def show(self):
        plt.show(block=False)
        #plt.show()

    def start(self):
        self.show()
        #self.thread.start()


class RawViewer(Viewer):
    def __init__(self, signal=None, refresh_freq=10.0, signal_boundaries=None, label_channels=None, number_display=1000):
        if signal_boundaries is None:
            signal_boundaries = [600000, 800000]
            #signal_boundaries = [700, 1000]
        super(RawViewer, self).__init__(refresh_freq, signal_boundaries)

        self.signal = signal
        self.label_channels = label_channels
        self.number_of_channels = len(self.label_channels)
        self.number_display = number_display

        self.figure, self.axes = plt.subplots(self.number_of_channels, 1, sharex=True, figsize=(15, 10))
        self.axes_plot = []
        formatter = mticker.FuncFormatter(timeTicks)

        times = np.linspace(0, 1, self.number_display)
        fake_data = np.zeros(self.number_display)

        for i, label in enumerate(self.label_channels):
            self.axes[i].set_title(label)
            ax_plot, = self.axes[i].plot(times, fake_data)
            self.axes_plot.append(ax_plot)
            self.axes[i].set_ylim([self.low, self.high])
            self.axes[i].xaxis.set_major_formatter(formatter)

        self.figure.canvas.draw()
        plt.ion()

    def refresh(self, data=None):
        if data is not None:
            signal_to_display = data
        elif isinstance(self.signal, AutoQueue):
            signal_to_display = self.signal.get()
        else:
            signal_to_display = self.signal

        signal_to_display.lock.acquire()
        signal_time = signal_to_display.time
        signal_data = signal_to_display.data
        signal_to_display.lock.release()

        times = np.linspace(signal_time[0], signal_time[-1], self.number_display)

        for i in range(self.number_of_channels):
            #y_signal = np.interp(times, signal_time, signal_data[i, :])
            #self.axes_plot[i].set_xdata(times)
            #self.axes_plot[i].set_ydata(y_signal)
            self.axes[i].set_ylim([np.mean(signal_data[i, 100:]) - 5.0 * np.std(signal_data[i, 100:]), np.mean(signal_data[i, 100:]) + 5.0 * np.std(signal_data[i, 100:])])
            #self.axes[i].set_ylim([np.min(signal_data[i, :]), np.max(signal_data[i, :])])
            self.axes_plot[i].set_data(signal_time, signal_data[i, :])
        self.axes[0].set_xlim(signal_time[0], signal_time[-1])

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()


class ButterFilterViewer(RawViewer):
    def __init__(self, signal=None, refresh_freq=10.0, signal_boundaries=None, label_channels=None, number_display=1000):
        super(ButterFilterViewer, self).__init__(signal, refresh_freq, signal_boundaries, label_channels, number_display)


class FFTViewer(Viewer):
    def __init__(self, signal=None, refresh_freq=10.0, signal_boundaries=None, label_channels=None):
        """
        Plots a Single-Sided Amplitude Spectrum of y(t)
        """
        if signal_boundaries is None:
            signal_boundaries = [0, 10000000]
        super(FFTViewer, self).__init__(refresh_freq, signal_boundaries)
        self.signal = signal

        self.label_channels = label_channels
        self.number_of_channels = len(self.label_channels)

        self.figure, self.axes = plt.subplots(self.number_of_channels, 1, figsize=(15, 10))
        self.axes_plot = []

        fake_freq, fake_data = range(100), np.zeros(100)

        for i, label in enumerate(self.label_channels):
            self.axes[i].set_title(label)
            ax_plot, = self.axes[i].plot(fake_freq, fake_data)
            self.axes_plot.append(ax_plot)
            self.axes[i].set_ylim([self.low, self.high])
            self.axes[i].set_xlim([0.0, 100.0])

        self.figure.canvas.draw()
        plt.ion()

    def refresh(self, data=None):
        if data is not None:
            signal_to_display = data
        elif isinstance(self.signal, AutoQueue):
            signal_to_display = self.signal.get()
        else:
            signal_to_display = self.signal

        signal_to_display.lock.acquire()
        signal_freq = signal_to_display.freq
        signal_data = abs(signal_to_display.data)**2
        signal_acq_freq = signal_to_display.estimated_acq_freq
        signal_to_display.lock.release()

        for i in range(self.number_of_channels):
            self.axes_plot[i].set_data(signal_freq, signal_data[i, :])
            self.axes[i].set_xlim(0.0, signal_acq_freq / 2.0)
            self.axes[i].set_ylim(0.0, np.max(signal_data[i, :]))
            #self.axes_plot[i].set_data(signal_freq, signal_data[i, :])
            #self.axes[i].set_xlim(signal_freq[0], signal_freq[-1])
            #self.axes[i].draw_artist(self.axes_plot[i])

        #self.figure.canvas.update()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

        #print signal_to_display.get_alpha_power()
