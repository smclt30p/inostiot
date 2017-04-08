import traceback

import serial


class ArdADC():

    PACKET_SIZE = 16
    BAUDRATE = 9600

    def __init__(self):

        try:
            self.serial = serial.Serial("COM5", timeout=5, baudrate=self.BAUDRATE)
        except BaseException as e:
            raise ArdADC.ArdADCException(e)

    def handshake(self):

        syn = self.serial.read(self.PACKET_SIZE)

        if self._checksum(syn) != syn[-1]:
            raise ArdADC.ArdADCException("SYN Checksum invalid")

        if self._get_data(syn) != "SYN":
            ArdADC.ArdADCException("SYN invalid")

        self.serial.write(self._make_packet("ACK"))
        self.serial.write(self._make_packet("SYN"))

        ack = self.serial.read(self.PACKET_SIZE)

        if self._checksum(ack) != ack[-1]:
            ArdADC.ArdADCException("ACK checksum invalid!")

        if self._get_data(ack) != "ACK":
            ArdADC.ArdADCException("ACK invalid")

    def _checksum(self, data):
        check = 0
        for i in range(0, self.PACKET_SIZE - 1):
            if (data[i]) % 2 == 0:
                check += 1
        return check

    def _make_packet(self, string):
        data = []
        for i in string:
            data.append(ord(i))
        for i in range(0, self.PACKET_SIZE - 1 - len(data)):
            data.append(0)
        data.append(self._checksum(data))
        return data

    def _get_data(self, incoming):

        if self._checksum(incoming) != incoming[-1]:
            raise ArdADC.ArdADCException("Invalid packet")

        data = []
        for i in incoming:
            if i == 0:  # null terminated
                string = ""
                for i in data:
                    string += i
                return string
            data.append(chr(i))

    def analog_read(self, pin):
        pass
        self.serial.write(self._make_packet("GET {}".format(pin)))
        print(self._get_data(self.serial.read(self.PACKET_SIZE)))

    class ArdADCException(BaseException):
        pass

if __name__ == "__main__":

    try:

        adc = ArdADC()
        adc.handshake()
        adc.analog_read(0)

    except ArdADC.ArdADCException:
        traceback.print_exc()

