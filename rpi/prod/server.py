from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import serial
import time

class RequestHandler(SimpleHTTPRequestHandler):

    data = None

    def do_GET(self):
        try:

            url = parse_qs(self.path)
            port = url["port"]

            if port is None or len(port) == 0:
                raise BaseException("Malformed URL!")

            self.data = int(port[0])

            if self.data > 5 or self.data < 0:
                raise BaseException("Invalid port!")

            read = Server.getADC().analog_read(self.data)

            if read == "NACK":
                raise BaseException("NACK from ADC")

            self.send_response(200)

            response = {"status":"ACK", "value": read }
            self.wfile.write(str(response).encode("utf-8"))

        except BaseException as e:
            self.write_exception(e)

    def write_exception(self, e):
        self.send_response(500)
        self.end_headers()
        data = {"status": "NACK", "detail": str(e)}
        self.wfile.write(str(data).encode("utf-8"))
        return

class Server(ThreadingMixIn, HTTPServer):
    
    adc = None
    
    @staticmethod
    def initADC():
        Server.adc = ADC("/dev/ttyUSB0")
        try:
            Server.adc.handshake()
        except BaseException as e:
            print(str(e))
            exit(-1)

        print("ADC OK!")

    @staticmethod
    def getADC():
        if Server.adc is None:
            Server.initADC()
        return Server.adc

class ADC():
    class ADCError(BaseException):
        pass

    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.serial = serial.Serial(self.interface, baudrate=9600)

    def handshake(self):

        try:
            syn = self.read_string()
            if syn not in "SYN":
                raise self.ADCError("Invalid SYN received: " + syn)
            self.write_string("ACK")
            self.write_string("SYN")
            ack = self.read_string()
            if ack not in "ACK":
                raise self.ADCError("Invalid ACK response: " + ack)
            return self.get_version()
        except BaseException as e:
            print("ADC connect fail, trying again...")
            time.sleep(1)
            return handshake()

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

if __name__ == "__main__":
    try:
        server = Server(('0.0.0.0', 80), RequestHandler)
        Server.getADC()
        server.serve_forever()
    except KeyboardInterrupt:
        if Server.adc is not None:
            Server.adc.close()
        print("Shutting down server...")
