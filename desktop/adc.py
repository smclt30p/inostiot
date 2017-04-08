import serial
from PyQt5.QtCore import QObject


class ADC(QObject):
    class ADCError(BaseException):
        pass

    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.serial = serial.Serial(self.interface, baudrate=250000)

    def handshake(self):
        if self.read_string() != "SYN":
            raise self.ADCError("Invalid greet received!")
        self.write_string("ACK")
        self.write_string("SYN")
        if self.read_string() != "ACK":
            raise self.ADCError("Invalid second greet response!")
        return self.get_version()

    def get_version(self):
        data = self.read_string()
        return data.replace("HELLO ", "")

    def read_string(self):
        data = ''
        while True:
            inc = self.serial.inWaiting()
            if inc == 0:
                continue
            data += self.serial.read(1).decode("utf-8")
            if data.endswith(";"):
                return data[:-1]

    def write_string(self, data):
        data += ';'
        self.serial.write(bytes(data, "utf-8"))
        self.serial.flush()

    def analog_read(self, port):
        self.write_string("GET {}".format(port))
        return self.read_string()

    def close(self):
        self.write_string("RESET")
        self.serial.close()