__author__ = 'benjamindeleener'
from numpy import fft


class MuseSignal(object):
    def __init__(self, length=200, do_fft=False):
        self.length = length
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
