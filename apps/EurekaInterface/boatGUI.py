import sys
import ctypes
from PyQt4 import QtGui, QtCore
import thread
import time
from datetime import datetime

from pymuse.ios import MuseIO, MuseIOError
from pymuse.signals import MultiChannelSignal
from pymuse.processes import Process
from pymuse.pipeline import Analyzer


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Course de bateaux")
        self.home()

    def home(self):
        # Define dimensions - Only works on windows ...
        #user32 = ctypes.windll.user32
        #user32.SetProcessDPIAware()
        #[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        [w, h] = [1500, 800]
        [w_btn, h_btn] = [100, 30]
        [w_label, h_label] = [100, 30]
        # Create labels
        self.status1_label = QtGui.QLabel(self)
        self.status1_label.setText("0 0 0 0 0 - 100%")
        self.status1_label.resize(w_label, h_label)
        self.status1_label.move(10, 0)
        self.status2_label = QtGui.QLabel(self)
        self.status2_label.setText("0 0 0 0 0 - 100%")
        self.status2_label.resize(w_label, h_label)
        self.status2_label.move(w-w_label, 0)
        self.speed1_label = QtGui.QLabel(self)
        self.speed1_pixmap = QtGui.QPixmap("j1_0.gif")
        self.speed1_pixmap_1 = QtGui.QPixmap("j1_1.gif")
        self.speed1_pixmap_2 = QtGui.QPixmap("j1_2.gif")
        self.speed1_pixmap_3 = QtGui.QPixmap("j1_3.gif")
        self.speed1_pixmap_4 = QtGui.QPixmap("j1_4.gif")
        self.speed1_pixmap_5 = QtGui.QPixmap("j1_5.gif")
        self.speed1_pixmap_6 = QtGui.QPixmap("j1_6.gif")
        self.speed1_label.setPixmap(self.speed1_pixmap)
        self.speed1_label.resize(self.speed1_pixmap.width(), self.speed1_pixmap.height())
        self.speed1_label.move(w/4-600/2, h/2-600/2)
        self.speed2_label = QtGui.QLabel(self)
        self.speed2_pixmap = QtGui.QPixmap("j2_0.gif")
        self.speed2_pixmap_1 = QtGui.QPixmap("j2_1.gif")
        self.speed2_pixmap_2 = QtGui.QPixmap("j2_2.gif")
        self.speed2_pixmap_3 = QtGui.QPixmap("j2_3.gif")
        self.speed2_pixmap_4 = QtGui.QPixmap("j2_4.gif")
        self.speed2_pixmap_5 = QtGui.QPixmap("j2_5.gif")
        self.speed2_pixmap_6 = QtGui.QPixmap("j2_6.gif")
        self.speed2_label.setPixmap(self.speed2_pixmap)
        self.speed2_label.resize(self.speed2_pixmap.width(), self.speed2_pixmap.height())
        self.speed2_label.move(3*w/4-600/2, h/2-600/2)
        # Create buttons
        self.exit_btn = QtGui.QPushButton("Quitter", self)
        self.exit_btn.resize(w_btn, h_btn)
        self.exit_btn.move(w/2-w_btn/2, h-2*h_btn)
        self.connect1_btn = QtGui.QPushButton("Connecter J1", self)
        self.connect1_btn.resize(w_btn, h_btn)
        self.connect1_btn.move(w/4-3*w_btn/2, h-2*h_btn)
        self.unconnect1_btn = QtGui.QPushButton("Deconnecter J1", self)
        self.unconnect1_btn.resize(w_btn, h_btn)
        self.unconnect1_btn.move(w/4+w_btn/2, h-2*h_btn)
        self.unconnect1_btn.setDisabled(True)
        self.connect2_btn = QtGui.QPushButton("Connecter J2", self)
        self.connect2_btn.resize(w_btn, h_btn)
        self.connect2_btn.move(3*w/4-3*w_btn/2, h-2*h_btn)
        self.unconnect2_btn = QtGui.QPushButton("Deconnecter J2", self)
        self.unconnect2_btn.resize(w_btn, h_btn)
        self.unconnect2_btn.move(3*w/4+w_btn/2, h-2*h_btn)
        self.unconnect2_btn.setDisabled(True)
        self.play_btn = QtGui.QPushButton("Jouer", self)
        self.play_btn.resize(w_btn, h_btn)
        self.play_btn.move(w/2-w_btn/2, h/2)
        # Associate callbacks
        self.exit_btn.clicked.connect(self.cb_close_app)
        self.play_btn.clicked.connect(self.cb_play)
        self.connect1_btn.clicked.connect(self.cb_connect1)
        self.unconnect1_btn.clicked.connect(self.cb_unconnect1)
        self.connect2_btn.clicked.connect(self.cb_connect2)
        self.unconnect2_btn.clicked.connect(self.cb_unconnect2)
        # Display window
        self.showFullScreen()

    def cb_close_app(self):
        # Make sure the Muse are disconnected
        # Close the GUI
        sys.exit()

    def cb_play(self):
        # Callback for when the game starts
        # Needs to update self.speedX_label when speed is changed. This is done by loading "jX_Y.gif" and displaying it,
        # with Y representing the speed level.
        # Needs to constantly update the connection status, which is, for each player, the text shown in the top corners
        # of the screen as "0 0 0 0 0 - 100%" initially. The 5 zeros represent the contact of the 5 electrodes, and
        # the 100% represents the battery life.
        # Needs to run for a set amount of time OR until a player has activated the contact detector at the finish line
        # At the end of execution, needs to put back the GUI in its initial state whilst keeping the Muse connected
        # Also, should verify if both Muse are connected or just one, since the game should be playable alone if needed
        print(" ")  # Dummy print

    def cb_connect1(self):
        # Needs to connect Muse to the program here
        # Verify that the connection is good
        # If the connection has failed, show an error message
        # If the connection is successful, disable the connect button and activate the unconnect one
        self.connect1_btn.setDisabled(True)
        self.unconnect1_btn.setEnabled(True)

    def cb_unconnect1(self):
        # Needs to disconnect the Muse and verify that the ports have been closed
        # If the disconnection is successful, disable the unconnect button and activate the connect one
        self.connect1_btn.setEnabled(True)
        self.unconnect1_btn.setDisabled(True)

    def cb_connect2(self):
        # Needs to connect Muse to the program here
        # Verify that the connection is good
        # If the connection has failed, show an error message
        # If the connection is successful, disable the connect button and activate the unconnect one
        self.connect2_btn.setDisabled(True)
        self.unconnect2_btn.setEnabled(True)

    def cb_unconnect2(self):
        # Needs to disconnect the Muse and verify that the ports have been closed
        # If the disconnection is successful, disable the unconnect button and activate the connect one
        self.connect2_btn.setEnabled(True)
        self.unconnect2_btn.setDisabled(True)

    def update_data(self, data):
        if 0.0 <= data < 0.17:
            self.speed1_label.setPixmap(self.speed1_pixmap_1)
        if 0.17 <= data < 0.33:
            self.speed1_label.setPixmap(self.speed1_pixmap_2)
        if 0.33 <= data < 0.5:
            self.speed1_label.setPixmap(self.speed1_pixmap_3)
        if 0.5 <= data < 0.67:
            self.speed1_label.setPixmap(self.speed1_pixmap_4)
        if 0.67 <= data < 0.83:
            self.speed1_label.setPixmap(self.speed1_pixmap_5)
        if 0.83 <= data <= 1:
            self.speed1_label.setPixmap(self.speed1_pixmap_6)
        return


def update_data(update_frequency=20.0, gui=None, signal=None, lock=None):
    update_timing = 1.0 / float(update_frequency)
    if gui is not None:
        times_web = 0.0
        while True:
            # put data in queue for HTML server to get it
            now = time.time()
            if now - times_web > 1.0 / update_frequency:
                analysis_frequency = 1.0 / (now - times_web)
                times_web = now

                if lock is not None:
                    lock.acquire()
                s = signal.data[0, -1]
                if lock is not None:
                    lock.release()
                gui.update_data(s)
                print 'I am updating my data', s, analysis_frequency
            else:
                time.sleep(0.5 / update_frequency)
        while True:

            time.sleep(update_timing)


def main():
    app = QtGui.QApplication(sys.argv)
    gui = Window()

    signals = dict()

    # EEG signal
    signal_concentration = MultiChannelSignal(length=300,
                                              estimated_acquisition_freq=10.0,
                                              label_channels=['Concentration'])

    update_frequency = 10.0

    try:
        thread.start_new_thread(update_data, (update_frequency, gui, signal_concentration, signal_concentration.lock))
    except:
        print "Error: unable to start thread"

    signals['concentration'] = signal_concentration

    # Initializing the server
    try:
        server = MuseIO(port=5001, signal=signals)
    except MuseIOError, err:
        print str(err)
        sys.exit(1)

    # Starting the server
    try:
        thread.start_new_thread(server.start, ())
    except KeyboardInterrupt:
        print "\nEnd of program: Caught KeyboardInterrupt"
        sys.exit(0)

    sys.exit(app.exec_())

main()





