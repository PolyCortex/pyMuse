__author__ = 'benjamindeleener'
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
import numpy as np
from utils import Thread
from Queue import Queue


def timeTicks(x, pos):
    d = timedelta(milliseconds=x)
    return str(d)


class Viewer(Thread):
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
        print 'plot show'
        #plt.show(block=False)
        plt.show()

    def start(self):
        self.show()
        self.thread.start()


class ViewerSignal(Viewer):
    def __init__(self, signal, window_duration=5000.0, refresh_freq=10.0, signal_boundaries=None):
        super(ViewerSignal, self).__init__(refresh_freq, signal_boundaries)
        self.signal = signal
        self.window_duration = window_duration
        self.number_of_channels = self.signal.number_of_channels

        self.figure, self.axes = plt.subplots(self.number_of_channels, 1, sharex=True, figsize=(15, 10))
        self.axes_plot = []
        formatter = mticker.FuncFormatter(timeTicks)

        self.signal.lock.acquire()
        signal_time, signal_data = self.signal.get_window_ms(length_window=self.window_duration)
        self.signal.lock.release()

        for i, label in enumerate(self.signal.label_channels):
            self.axes[i].set_title(label)
            ax_plot, = self.axes[i].plot(signal_time, signal_data[i, :])
            self.axes_plot.append(ax_plot)
            self.axes[i].set_ylim([self.low, self.high])
            self.axes[i].xaxis.set_major_formatter(formatter)

        plt.ion()

    def refresh(self):
        while True:
            time_now = datetime.now()
            if (time_now - self.last_refresh).total_seconds() > 1.0 / self.refresh_freq:
                self.last_refresh = time_now
                pass
            else:
                return

            self.signal.lock.acquire()
            signal_time, signal_data = self.signal.get_window_ms(length_window=self.window_duration)
            self.signal.lock.release()
            for i in range(self.number_of_channels):
                self.axes_plot[i].set_ydata(signal_data[i, :])
                times = np.linspace(signal_time[0], signal_time[-1], len(signal_time))
                self.axes_plot[i].set_xdata(times)
            self.axes[0].set_xlim(signal_time[0], signal_time[-1])

            self.figure.canvas.draw()
            self.figure.canvas.flush_events()


class ViewerFrequencySpectrum(Viewer):
    def __init__(self, signal, refresh_freq=10.0, signal_boundaries=None, label_channels=None):
        """
        Plots a Single-Sided Amplitude Spectrum of y(t)
        """
        super(ViewerFrequencySpectrum, self).__init__(refresh_freq, signal_boundaries)
        self.signal = signal

        self.label_channels = label_channels
        self.number_of_channels = len(self.label_channels)

        self.figure, self.axes = plt.subplots(self.number_of_channels, 1, sharex=True, figsize=(15, 10))
        self.axes_plot = []
        formatter = mticker.FuncFormatter(timeTicks)

        fake_freq, fake_data = range(10), np.zeros(10)

        for i, label in enumerate(self.label_channels):
            self.axes[i].set_title(label)
            ax_plot, = self.axes[i].plot(fake_freq, fake_data)
            self.axes_plot.append(ax_plot)
            self.axes[i].set_ylim([self.low, self.high])
            self.axes[i].xaxis.set_major_formatter(formatter)

        plt.ion()

    def refresh(self):
        while True:
            time_now = datetime.now()
            if (time_now - self.last_refresh).total_seconds() > 1.0 / self.refresh_freq:
                self.last_refresh = time_now
                pass
            else:
                return

            if isinstance(self.signal, Queue):
                signal_to_display = self.signal.get()
            else:
                signal_to_display = self.signal

            signal_to_display.lock.acquire()
            signal_freq = signal_to_display.freq
            signal_data = abs(signal_to_display.data)
            signal_to_display.lock.release()
            for i in range(self.number_of_channels):
                self.axes_plot[i].set_ydata(signal_data[i, :])
                self.axes_plot[i].set_xdata(signal_freq)
            self.axes[0].set_xlim(signal_freq[0], signal_freq[-1])

            self.figure.canvas.draw()
            self.figure.canvas.flush_events()


class ViewerMuseEEG(Viewer):
    def __init__(self, signal, acquisition_freq, signal_boundaries=None):
        super(ViewerMuseEEG, self).__init__(acquisition_freq, signal_boundaries)
        self.signal = signal

        self.figure, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(4, 1, sharex=True, figsize=(15, 10))
        self.ax1.set_title('Left ear')
        self.ax2.set_title('Left forehead')
        self.ax3.set_title('Right forehead')
        self.ax4.set_title('Right ear')

        self.ax1_plot, = self.ax1.plot(self.signal.time, self.signal.l_ear)
        self.ax2_plot, = self.ax2.plot(self.signal.time, self.signal.l_forehead)
        self.ax3_plot, = self.ax3.plot(self.signal.time, self.signal.r_forehead)
        self.ax4_plot, = self.ax4.plot(self.signal.time, self.signal.r_ear)

        self.ax1.set_ylim([self.low, self.high])
        self.ax2.set_ylim([self.low, self.high])
        self.ax3.set_ylim([self.low, self.high])
        self.ax4.set_ylim([self.low, self.high])

        formatter = mticker.FuncFormatter(timeTicks)
        self.ax1.xaxis.set_major_formatter(formatter)
        self.ax2.xaxis.set_major_formatter(formatter)
        self.ax3.xaxis.set_major_formatter(formatter)
        self.ax4.xaxis.set_major_formatter(formatter)

        plt.ion()

    def show(self):
        plt.show(block=False)
        self.refresh()

    def refresh(self):
        time_now = datetime.now()
        if (time_now - self.last_refresh).total_seconds() > self.refresh_freq:
            self.last_refresh = time_now
            pass
        else:
            return

        self.ax1_plot.set_ydata(self.signal.l_ear)
        self.ax2_plot.set_ydata(self.signal.l_forehead)
        self.ax3_plot.set_ydata(self.signal.r_forehead)
        self.ax4_plot.set_ydata(self.signal.r_ear)

        times = list(np.linspace(self.signal.time[0], self.signal.time[-1], self.signal.length))
        self.ax1_plot.set_xdata(times)
        self.ax2_plot.set_xdata(times)
        self.ax3_plot.set_xdata(times)
        self.ax4_plot.set_xdata(times)

        self.ax1.set_xlim(self.signal.time[0], self.signal.time[-1])

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()


class MuseViewerConcentrationMellow(object):
    def __init__(self, signal_concentration, signal_mellow, signal_boundaries=None):
        self.refresh_freq = 0.05
        self.init_time = 0.0
        self.last_refresh = datetime.now()
        self.signal_concentration = signal_concentration
        self.signal_mellow = signal_mellow

        if signal_boundaries is not None:
            self.low, self.high = signal_boundaries[0], signal_boundaries[1]
        else:
            self.low, self.high = 0, 1

        self.x_data_concentration = range(0, self.signal_concentration.length, 1)
        self.x_data_mellow = range(0, self.signal_mellow.length, 1)
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, sharex=True, figsize=(15, 10))
        self.ax1.set_title('Concentration')
        self.ax2.set_title('Mellow')

        self.ax1_plot, = self.ax1.plot(self.x_data_concentration, self.signal_concentration.concentration)
        self.ax2_plot, = self.ax2.plot(self.x_data_mellow, self.signal_mellow.mellow)

        self.ax1.set_ylim([self.low, self.high])
        self.ax2.set_ylim([self.low, self.high])

        formatter = mticker.FuncFormatter(timeTicks)
        self.ax1.xaxis.set_major_formatter(formatter)
        self.ax2.xaxis.set_major_formatter(formatter)

        plt.ion()

    def show(self):
        plt.show(block=False)
        self.refresh()

    def refresh(self):
        time_now = datetime.now()
        if (time_now - self.last_refresh).total_seconds() > self.refresh_freq:
            self.last_refresh = time_now
            pass
        else:
            return

        self.ax1_plot.set_ydata(self.signal_concentration.concentration)
        self.ax2_plot.set_ydata(self.signal_mellow.mellow)

        times = list(np.linspace(self.signal_concentration.time[0], self.signal_concentration.time[-1], self.signal_concentration.length))
        self.ax1_plot.set_xdata(times)
        self.ax2_plot.set_xdata(times)

        plt.xlim(self.signal_concentration.time[0], self.signal_concentration.time[-1])

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
