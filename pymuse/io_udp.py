__author__ = 'benjamindeleener'
import socket


class MuseIOUDP():
    def __init__(self, port, signal=None, viewer=None):
        self.signal = signal
        self.viewer = viewer
        self.game = None
        self.port = port
        self.udp_ip = '127.0.0.1'

    def initializePort(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.udp_ip, self.port))
        print 'Port started to listen'
        while True:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            print data


if __name__ == "__main__":
    io_udp = MuseIOUDP(5000)
    io_udp.initializePort()
