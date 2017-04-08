import traceback

import serial


class ArdADC():

    def __init__(self):

        try:
            self.serial = serial.Serial("/dev/ttyUSB0", timeout=5, baudrate=9600)
        except BaseException as e:
            raise ArdADC.ArdADCException(e)

    def handshake(self):

        syn = self.serial.read(32)

        if self.checksum(syn) != syn[-1]:
            raise ArdADC.ArdADCException("SYN Checksum invalid")

        if self.get_data(syn) != "SYN":
            ArdADC.ArdADCException("SYN invalid")

        self.serial.write(self.make_packet("ACK"))
        self.serial.write(self.make_packet("SYN"))

        ack = self.serial.read(32)

        if self.checksum(ack) != ack[-1]:
            ArdADC.ArdADCException("ACK checksum invalid!")

        if self.get_data(ack) != "ACK":
            ArdADC.ArdADCException("ACK invalid")

    def checksum(self, data):
        check = 0
        for i in range(0, 31):
            if (data[i]) % 2 == 0:
                check += 1
        return check

    def make_packet(self, string):
        data = []
        for i in string:
            data.append(ord(i))
        for i in range(0, 31 - len(data)):
            data.append(0)
        data.append(self.checksum(data))
        return data

    def get_data(self, incoming):
        data = []
        for i in incoming:
            if i == 0:  # null terminated
                string = ""
                for i in data:
                    string += i
                return string
            data.append(chr(i))

    class ArdADCException(BaseException):
        pass

if __name__ == "__main__":

    try:

        adc = ArdADC()
        adc.handshake()

    except ArdADC.ArdADCException:
        traceback.print_exc()

