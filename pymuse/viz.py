__author__ = 'benjamindeleener'
import matplotlib.pyplot as plt
from datetime import datetime

class MuseViewerSignal(object):
    def __init__(self, signal, signal_boundaries=None):
        self.refresh_freq = 0.15
        self.last_refresh = datetime.now()
        self.signal = signal
        if signal_boundaries is not None:
            self.low, self.high = signal_boundaries[0], signal_boundaries[1]
        else:
            self.low, self.high = 600, 1200

        self.x_data = range(0, self.signal.length, 1)
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
            self.ax1_plot, = self.ax1.plot(self.x_data, self.signal.l_ear)
            self.ax2_plot, = self.ax2.plot(self.x_data, self.signal.l_forehead)
            self.ax3_plot, = self.ax3.plot(self.x_data, self.signal.r_forehead)
            self.ax4_plot, = self.ax4.plot(self.x_data, self.signal.r_ear)

            self.ax1.set_ylim([self.low, self.high])
            self.ax2.set_ylim([self.low, self.high])
            self.ax3.set_ylim([self.low, self.high])
            self.ax4.set_ylim([self.low, self.high])

        plt.ion()

    def show(self):
        plt.show(block=False)

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

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()


class MuseViewerConcentrationMellow(object):
    def __init__(self, signal_concentration, signal_mellow, signal_boundaries=None):
        self.refresh_freq = 0.01
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

        plt.ion()

    def show(self):
        plt.show(block=False)

    def refresh(self):
        time_now = datetime.now()
        if (time_now - self.last_refresh).total_seconds() > self.refresh_freq:
            self.last_refresh = time_now
            pass
        else:
            return

        self.ax1_plot.set_ydata(self.signal_concentration.concentration)
        self.ax2_plot.set_ydata(self.signal_mellow.mellow)

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
