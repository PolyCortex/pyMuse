from pythonosc import dispatcher, osc_server
from datetime import datetime
from Queue import Queue

DEFAULT_PORT = 5001
LOCALHOST = '127.0.0.1'

class MuseInputStream():
    def __init__(self, port = DEFAULT_PORT, ip = LOCALHOST):
        self.signals = dict()

        dispatcher = dispatcher.Dispatcher()
        dispatcher.map("/muse/eeg", callback, 'eeg')
        server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
        server.serve_forever()
    
    def callback(self, *args): #Le dernier argument sera la signalName
        for i, arg in args[::-1]:
            if (i == 0):
                signal_name = arg
            else:
                if(signal_name not in self.signals):
                    self.signals[signal_name] = Signal()
                self.signals[signal_name].addData(arg)
                

                

class Signal():
    def __init__(self, length):
        self.init_time = datetime.now()
        self.data = Queue(length)
    
    def add(self, *args):
        

