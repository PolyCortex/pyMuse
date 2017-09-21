__author__ = 'benjamindeleener'

has_oscserver = True
try:
    from OSC import OSCServer, OSCError
except ImportError:
    has_oscserver = False

import types
import time
import timeit
from datetime import datetime, timedelta


# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is
# set to False
def handle_timeout(self):
    self.timed_out = True


class MuseIOError(OSCError):
    def __init__(self):
        super(MuseIOError, self).__init__()


class MuseIO():
    def __init__(self, port=5001, signal=None):
        self.signal = signal
        self.port = port
        self.udp_ip = '127.0.0.1'

        if not has_oscserver:
            raise Exception('ERROR: OSC not found')

        self.server = OSCServer((self.udp_ip, self.port))
        self.server.timeout = 0
        self.current_sample_id = 0
        self.init_time = None
        self.sample_rate = 220.0

        # funny python's way to add a method to an instance of a class
        self.server.handle_timeout = types.MethodType(handle_timeout, self.server)

        # add message handlers
        if 'eeg' in self.signal:
            self.server.addMsgHandler('/muse/eeg', self.callback_eeg_raw)
        if 'concentration' in self.signal:
            self.server.addMsgHandler('/muse/elements/experimental/concentration', self.callback_concentration)
        if 'mellow' in self.signal:
            self.server.addMsgHandler('/muse/elements/experimental/mellow', self.callback_mellow)
        self.server.addMsgHandler("default", self.default_handler)

    def default_handler(self, addr, tags, stuff, source):
        # nothing to do here. This function is called for all messages that are not supported by the application.
        #print "SERVER: No handler registered for ", addr
        return None

    def callback_eeg_raw(self, path, tags, args, source):
        # which user will be determined by path:
        # we just throw away all slashes and join together what's left
        # tags will contain 'ffff'
        # args is a OSCMessage with data
        # source is where the message came from (in case you need to reply)
        self.signal['eeg'].lock.acquire()
        self.signal['eeg'].id = self.current_sample_id
        self.signal['eeg'].add_data(args, add_time=False)
        self.signal['eeg'].add_time(time.time())
        self.signal['eeg'].add_datetime(datetime.now())
        self.signal['eeg'].lock.release()

    def callback_concentration(self, path, tags, args, source):
        if 'concentration' in self.signal:
            self.signal['concentration'].lock.acquire()
            self.signal['concentration'].id = self.current_sample_id
            self.signal['concentration'].add_data(args, add_time=False)
            self.signal['concentration'].add_time(time.time())
            self.signal['concentration'].add_datetime(datetime.now())
            self.signal['concentration'].lock.release()

    def callback_mellow(self, path, tags, args, source):
        if 'mellow' in self.signal:
            self.signal['mellow'].lock.acquire()
            self.signal['mellow'].id = self.current_sample_id
            self.signal['mellow'].add_data(args, add_time=False)
            self.signal['mellow'].add_time(time.time())
            self.signal['mellow'].add_datetime(datetime.now())
            self.signal['mellow'].lock.release()

    def handle_request(self):
        # clear timed_out flag
        self.server.timed_out = False
        # handle all pending requests then return
        while not self.server.timed_out:
            self.server.handle_request()

    def start(self, freq=220):
        update_timing = 1.0/float(freq)
        while True:
            try:
                time.sleep(update_timing)
                self.handle_request()
            except KeyboardInterrupt:
                import sys
                print('KeyboardInterrupt on line {}'.format(sys.exc_info()[-1].tb_lineno))
                sys.exit(2)
            except Exception as e:
                import sys
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                print(str(e))
                sys.exit(2)


class UDPIO(object):
    def __init__(self, freq=220.0, udp_ip='127.0.0.1', udp_port=5005, index_channels=None, signal=None, channels=None):
        self.signal = signal

        self.udp_ip = udp_ip
        self.udp_port = udp_port

        self.channels = channels
        self.index_channels = index_channels
        if self.index_channels is None:
            self.index_channels = range(0, 4)

    def start(self):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.udp_ip, self.udp_port))
        while True:
            data, addr = sock.recvfrom(512)  # buffer size is 1024 bytes
            voltage_values = [float(d) for d in data.split(', ')]

            self.signal['eeg'].lock.acquire()
            self.signal['eeg'].add_data(voltage_values)
            self.signal['eeg'].lock.release()



"""
class RPiMCP300XIO(object):
    def __init__(self, signalclk=None, cs=None, miso=None, mosi=None, spi=None, gpio=None):
        '''Initialize MAX31855 device with software SPI on the specified CLK,
        CS, and DO pins.  Alternatively can specify hardware SPI by sending an
        Adafruit_GPIO.SPI.SpiDev device in the spi parameter.
        '''
        import Adafruit_GPIO as GPIO
        import Adafruit_GPIO.SPI as SPI

        self.signal = signal

        self._spi = None
        # Handle hardware SPI
        if spi is not None:
            self._spi = spi
        elif clk is not None and cs is not None and miso is not None and mosi is not None:
            # Default to platform GPIO if not provided.
            if gpio is None:
                gpio = GPIO.get_platform_gpio()
            self._spi = SPI.BitBang(gpio, clk, mosi, miso, cs)
        else:
            raise ValueError(
                'Must specify either spi for for hardware SPI or clk, cs, miso, and mosi for softwrare SPI!')
        self._spi.set_clock_hz(1000000)
        self._spi.set_mode(0)
        self._spi.set_bit_order(SPI.MSBFIRST)

    def read_adc(self, adc_number):
        '''Read the current value of the specified ADC channel (0-7).  The values
        can range from 0 to 1023 (10-bits).
        '''
        assert 0 <= adc_number <= 7, 'ADC number must be a value of 0-7!'
        # Build a single channel read command.
        # For example channel zero = 0b11000000
        command = 0b11 << 6  # Start bit, single channel read
        command |= (adc_number & 0x07) << 3  # Channel number (in 3 bits)
        # Note the bottom 3 bits of command are 0, this is to account for the
        # extra clock to do the conversion, and the low null bit returned at
        # the start of the response.
        resp = self._spi.transfer([command, 0x0, 0x0])
        # Parse out the 10 bits of response data and return it.
        result = (resp[0] & 0x01) << 9
        result |= (resp[1] & 0xFF) << 1
        result |= (resp[2] & 0x80) >> 7
        return result & 0x3FF

    def read(self, channel):
        assert 0 <= channel <= 4, 'ADC number must be a value of 0-7!'
        r = self._spi.xfer2([1, (8 + channel) << 4, 0])
        out = ((r[1] & 3) << 8) + r[2]
        return out

    def voltage(self, channel):
        return self._vref * self.read(channel) / 1024.0

    def start(self, freq=220):
        update_timing = 1.0 / float(freq)
        while True:
            try:
                time.sleep(update_timing)
                self.handle_request()
            except KeyboardInterrupt:
                import sys
                print('KeyboardInterrupt on line {}'.format(sys.exc_info()[-1].tb_lineno))
                sys.exit(2)
            except Exception as e:
                import sys
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                print(str(e))
                sys.exit(2)
"""

class OpenBCIIO(object):
    def __init__(self, port_name=None, baud=115200, index_channels=None, signal=None, channels=None):
        import openbci.open_bci_v3 as bci

        self.signal = signal

        self.port_name = port_name
        self.baud = baud

        self.channels = channels
        self.index_channels = index_channels
        if self.index_channels is None:
            self.index_channels = range(0, 8)

        self.nb_samples_out = -1
        self.tick = timeit.default_timer()
        self.start_tick = self.tick

        self.board = bci.OpenBCIBoard(port=self.port_name, scaled_output=False, log=True, filter_data=True)
        print("Board Instantiated")
        self.board.ser.write('v')
        self.sample_rate = float(self.board.getSampleRate())
        print 'Sample Rate: ', self.sample_rate
        time.sleep(5)

        self.current_sample_id = 0
        self.init_sample_id = 0
        self.init_time = None  # datetime.now()

    def start(self):
        self.board.start_streaming(self.callback_rawdata)

    def callback_rawdata(self, sample):
        id = sample.id
        if self.init_time is None:
            self.init_sample_id = id
            self.init_time = datetime.now()

        data = sample.channel_data
        data_to_save = [data[ind] for ind in self.index_channels]
        self.signal['eeg'].lock.acquire()
        self.signal['eeg'].id = sample.id
        self.signal['eeg'].add_data(data_to_save, add_time=False)
        self.signal['eeg'].add_time((self.current_sample_id + sample.id) / self.sample_rate)
        self.signal['eeg'].add_datetime(self.init_time + timedelta(seconds=(self.current_sample_id + sample.id - self.init_sample_id) / self.sample_rate))
        self.signal['eeg'].lock.release()
        if sample.id == 255:
            self.current_sample_id += 256

    def printData(self, sample):
        print "----------------"
        print("%f" % (sample.id))
        print sample.channel_data
        print sample.aux_data
        print "----------------"

        new_tick = timeit.default_timer()
        elapsed_time = new_tick - self.tick
        current_samples_out = self.nb_samples_out
        print "--- at t: ", (new_tick - self.start_tick), " ---"
        print "elapsed_time: ", elapsed_time
        print "nb_samples_out: ", current_samples_out - self.nb_samples_out
        sampling_rate = (current_samples_out - self.nb_samples_out) / elapsed_time
        print "sampling rate: ", sampling_rate
        self.tick = new_tick

if __name__ == "__main__":
    io_udp = MuseIO()
    io_udp.start()

