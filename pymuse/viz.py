__author__ = 'benjamindeleener'
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
from numpy import linspace


def timeTicks(x, pos):
    d = timedelta(milliseconds=x)
    return str(d)


class MuseViewer(object):
    def __init__(self, acquisition_freq, signal_boundaries=None):
        self.refresh_freq = 0.4  # default=0.15
        self.acquisition_freq = acquisition_freq
        self.init_time = datetime.now()
        self.last_refresh = datetime.now()

        if signal_boundaries is not None:
            self.low, self.high = signal_boundaries[0], signal_boundaries[1]
        else:
            self.low, self.high = 0, 1

class MuseViewerSignal(MuseViewer):
    def __init__(self, signal, acquisition_freq, signal_boundaries=None):
        super(MuseViewerSignal, self).__init__(acquisition_freq, signal_boundaries)
        self.signal = signal

        self.figure, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(4, 1, sharex=True, figsize=(15, 10))
        self.ax1.set_title('Left ear')
        self.ax2.set_title('Left forehead')
        self.ax3.set_title('Right forehead')
        self.ax4.set_title('Right ear')

        if self.signal.do_fft:
            self.ax1_plot, = self.ax1.plot(self.x_data[0:len(self.x_data)/2], self.signal.l_ear_fft[0:len(self.x_data)/2])
            self.ax2_plot, = self.ax2.plot(self.x_data[0:len(self.x_data)/2], self.signal.l_forehead_fft[0:len(self.x_data)/2])
            self.ax3_plot, = self.ax3.plot(self.x_data[0:len(self.x_data)/2], self.signal.r_forehead_fft[0:len(self.x_data)/2])
            self.ax4_plot, = self.ax4.plot(self.x_data[0:len(self.x_data)/2], self.signal.r_ear_fft[0:len(self.x_data)/2])

            self.ax1.set_ylim([0, 10000])
            self.ax2.set_ylim([0, 10000])
            self.ax3.set_ylim([0, 10000])
            self.ax4.set_ylim([0, 10000])
        else:
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

        if self.signal.do_fft:
            self.ax1_plot.set_ydata(self.signal.l_ear_fft[0:len(self.x_data)/2])
            self.ax2_plot.set_ydata(self.signal.l_forehead_fft[0:len(self.x_data)/2])
            self.ax3_plot.set_ydata(self.signal.r_forehead_fft[0:len(self.x_data)/2])
            self.ax4_plot.set_ydata(self.signal.r_ear_fft[0:len(self.x_data)/2])
        else:
            self.ax1_plot.set_ydata(self.signal.l_ear)
            self.ax2_plot.set_ydata(self.signal.l_forehead)
            self.ax3_plot.set_ydata(self.signal.r_forehead)
            self.ax4_plot.set_ydata(self.signal.r_ear)

            times = list(linspace(self.signal.time[0], self.signal.time[-1], self.signal.length))
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

        times = list(linspace(self.signal_concentration.time[0], self.signal_concentration.time[-1], self.signal_concentration.length))
        self.ax1_plot.set_xdata(times)
        self.ax2_plot.set_xdata(times)

        plt.xlim(self.signal_concentration.time[0], self.signal_concentration.time[-1])

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
