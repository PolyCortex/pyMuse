__author__ = 'benjamindeleener'

import sys
import time
from pymuse.ios import MuseServer
from pymuse.viz import MuseViewer
from pymuse.signal import MuseSignal
from liblo import ServerError


def main():
    signal = MuseSignal(length=500, do_fft=False)
    viewer = MuseViewer(signal, signal_boundaries=[0, 1])  # [600, 1200]

    try:
        server = MuseServer(signal, viewer)
    except ServerError, err:
        print str(err)
        sys.exit(1)

    viewer.show()

    server.start()
    while 1:
        time.sleep(0.01)

if __name__ == "__main__":
    main()
