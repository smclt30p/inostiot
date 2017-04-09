import sys
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs
import time
from core.ardadc import ArdADC


class RequestHandler(SimpleHTTPRequestHandler):

    data = None

    def do_GET(self):
        try:

            url = parse_qs(self.path)
            print(url.params)
            port = url["port"]

            if port is None or len(port) == 0:
                raise BaseException("Malformed URL!")

            self.data = int(port[0])

            if self.data > 5 or self.data < 0:
                raise BaseException("Invalid port!")

            read = Server.getADC(sys.argv[1]).analog_read(self.data)
            self.send_response(200)
            self.end_headers()
            response = {"status":"OK", "value": read }
            self.wfile.write(str(response).encode("utf-8"))

        except BaseException as e:
            self.write_exception(e)

    def log_message(self, format, *args):
        return

    def write_exception(self, e):
        self.send_response(500)
        self.end_headers()
        data = {"status": "ERR", "detail": str(e)}
        self.wfile.write(str(data).encode("utf-8"))
        return

class Server(ThreadingMixIn, HTTPServer):
    
    adc = None
    
    @staticmethod
    def initADC(port):

        failed = 0

        while True:
            try:
                Server.adc = ArdADC(port)
                break
            except BaseException:
                print("\rADC not found ({})".format(failed))
                failed += 1
                time.sleep(5)

        try:
            Server.adc.handshake()
        except BaseException as e:
            print(str(e))
            exit(-1)

        print("ADC OK!")

    @staticmethod
    def getADC(port):
        if Server.adc is None:
            Server.initADC(port)
        return Server.adc

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Missing port argument! COMX for Windows, /dev/xxx for POSIX")
        exit(-1)

    try:
        server = Server(('0.0.0.0', 80), RequestHandler)
        Server.getADC(sys.argv[1])
        server.serve_forever()

    except KeyboardInterrupt:
        if Server.adc is not None:
            Server.adc.close()
        print("Shutting down server...")
