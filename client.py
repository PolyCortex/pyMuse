from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from threading import Thread
import time

from pymuse.inputstream.muse_constants import MUSE_OSC_PATH

disp = Dispatcher()
start_time = time.time()
disp.map('/eeg', (lambda data1, data2, data3, data4, data5: print(time.time()- start_time)))

client = SimpleUDPClient('127.0.0.1', 5001)
#server = ThreadingOSCUDPServer(("127.0.0.1", 5001), disp)

def start_client():
    start = time.time()
    for i in range(256*4):
        client.send_message('/eeg', (i, i, i, i))
        time.sleep(1/256)
    print("Client exec time: " + str(time.time() - start))

#Thread(target=server.serve_forever).start()        
start_client()
