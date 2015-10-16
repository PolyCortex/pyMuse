__author__ = 'benjamindeleener'

import sys
import time
from pymuse.ios import MuseServer
from pymuse.viz import MuseViewerSignal, MuseViewerConcentrationMellow
from pymuse.signals import MuseEEG, MuseConcentration, MuseMellow
from liblo import ServerError


def main():
    # initialization of variables
    signals, viewers = dict(), dict()

    # Concentration and Mellow
    signal_concentration = MuseConcentration(length=400, acquisition_freq=10.0)
    signal_mellow = MuseMellow(length=400, acquisition_freq=10.0)
    viewer_concentration_mellow = MuseViewerConcentrationMellow(signal_concentration, signal_mellow, signal_boundaries=[-0.05, 1.05])

    signals['concentration'] = signal_concentration
    signals['mellow'] = signal_mellow
    viewers['concentration-mellow'] = viewer_concentration_mellow

    # Initializing the server
    try:
        server = MuseServer(port=5001, signal=signals, viewer=viewers)
    except ServerError, err:
        print str(err)
        sys.exit(1)

    import apps.pong.pong as pong
    pong_game = pong.PongApp()
    server.game = pong_game

    # Starting the server
    try:
        server.start()
        pong_game.run()
        while 1:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print "\nEnd of program: Caught KeyboardInterrupt"
        sys.exit(0)

if __name__ == "__main__":
    main()
