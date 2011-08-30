from twisted.internet import reactor, serialport
from twisted.python import log

from zope.interface import implements
from fizzjik.input.sonmicro import SonMicroSM130Protocol
from sparked.hardware import serial



class RFIDMonitor (serial.SerialPortMonitor):

    def __init__(self):
        serial.SerialPortMonitor.__init__(self)
        self.readers = {}


    def deviceAdded(self, dev):

        def found(result):
            protocol, baudrate = result
            device = serialport.SerialPort(protocol(self), dev['device'], reactor, baudrate)
            self.readers[dev['udi']] = device
            print device

        probe = serial.SerialProbe(dev['device'])
        probe.addCandidate(RFIDReaderProtocol, 19200)
        d = probe.start()
        d.addCallbacks(found, log.err)


    def deviceRemoved(self, d):
        if d['udi'] not in self.readers:
            return
        print "bye"
        del self.readers[d['udi']]


class RFIDReaderProtocol (SonMicroSM130Protocol):
    implements (serial.IProtocolProbe)

    probeRequest = "\xFF\x00\x01\x83\x84"
    probeResponse = "\xFF\x00\x02\x83\x4E\xD3"


