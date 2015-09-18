__author__ = 'benjamindeleener'
from numpy import fft, linspace
from datetime import datetime

class MuseSignal(object):
    def __init__(self, length, acquisition_freq):
        self.length = length
        self.acquisition_freq = acquisition_freq
        self.init_time = datetime.now()
        self.time = linspace(-float(self.length) / self.acquisition_freq + 1.0 / self.acquisition_freq, 0.0,
                               self.length)


class MuseEEG(MuseSignal):
    def __init__(self, length=200, acquisition_freq=220, do_fft=False):
        super(MuseEEG, self).__init__(length, acquisition_freq)
        self.do_fft = do_fft
        self.l_ear, self.l_forehead, self.r_forehead, self.r_ear = [0.0] * self.length, [0.0] * self.length, [
            0.0] * self.length, [0.0] * self.length
        self.l_ear_fft, self.l_forehead_fft, self.r_forehead_fft, self.r_ear_fft = [0.0] * self.length, [0.0] * self.length, [
            0.0] * self.length, [0.0] * self.length

    def add_l_ear(self, s):
        self.l_ear.append(s)
        del self.l_ear[0]
        if self.do_fft:
            self.l_ear_fft = fft.fft(self.l_ear)

    def add_l_forehead(self, s):
        self.l_forehead.append(s)
        del self.l_forehead[0]
        if self.do_fft:
            self.l_forehead_fft = fft.fft(self.l_forehead)

    def add_r_forehead(self, s):
        self.r_forehead.append(s)
        del self.r_forehead[0]
        if self.do_fft:
            self.r_forehead_fft = fft.fft(self.r_forehead)

    def add_r_ear(self, s):
        self.r_ear.append(s)
        del self.r_ear[0]
        if self.do_fft:
            self.r_ear_fft = fft.fft(self.r_ear)

    def add_time(self):
        self.time.append(1.0 / self.acquisition_freq)
        del self.time[0]


class MuseConcentration(object):
    def __init__(self, length=200):
        self.length = length
        self.concentration = [0.0] * self.length

    def add_concentration(self, s):
        self.concentration.append(s)
        del self.concentration[0]


class MuseMellow(object):
    def __init__(self, length=200):
        self.length = length
        self.mellow = [0.0] * self.length

    def add_mellow(self, s):
        self.mellow.append(s)
        del self.mellow[0]
