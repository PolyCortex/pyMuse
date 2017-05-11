import sys
import ctypes  # Only works on Windows?
from PyQt4 import QtGui, QtCore


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("PolyCortex - Course de bateaux")
        self.home()

    def home(self):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        [w_btn, h_btn] = [100, 30]
        exit_btn = QtGui.QPushButton("Quitter", self)
        exit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        exit_btn.resize(w_btn, h_btn)
        exit_btn.move(w/2-w_btn/2, h-2*h_btn)
        self.showFullScreen()


def main():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec_())


main()





