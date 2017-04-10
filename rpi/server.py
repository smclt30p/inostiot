import sys
import traceback
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlsplit
import time
from core.ardadc import ArdADC


class RequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        try:

            url = urlsplit(self.path)

            query = url.query

            if len(query) == 0:
                self.write_version()

            query_split = query.split("=")

            if len(query_split) == 1:

                if "version" in query:
                    self.write_version()
                else:
                    raise BaseException("Malformed request!")

            elif len(query_split) == 2:
                if "port" in query_split[0]:

                    ports = []

                    for port in query_split[1].split(","):

                        port = int(port)

                        if port > 5 or port < 0:
                            raise BaseException("Invalid port!")

                        ports.append( { "port":port, "value":
                            Server.getADC(sys.argv[1]).analog_read(port)} )


                    self.send_response(200)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = {"status": "OK", "rdata": ports}
                    self.wfile.write(str(response).encode("utf-8"))

            else:
                raise BaseException("Malformed request!")

        except BaseException as e:
            traceback.print_exc()
            self.write_exception(e)

    def write_version(self):
        self.send_response(200)
        self.end_headers()
        response = {"status": "OK", "version": "v1.0"}
        self.wfile.write(str(response).encode("utf-8"))

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
