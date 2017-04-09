import demjson
import requests
import time
from PyQt5.QtCore import QThread, pyqtSignal


class GraphWorker(QThread):

    signal = pyqtSignal(int, float)
    timebase = 1
    running = True

    def __init__(self,ip, graph, initial):
        super().__init__()

        self.timebase = initial
        self.ip = ip

        self.graph = graph
        self.graph.addDataset("#FF0000")
        self.graph.addDataset("#00FF00")
        self.graph.addDataset("#0000FF")
        self.graph.addDataset("#FFFF00")
        self.graph.addDataset("#FF00FF")
        self.graph.addDataset("#00FFFF")

    def run(self):

        json = demjson.JSON()

        try:
            while self.running:

                response = requests.get("http://{}/api?port=0,1,2,3,4,5".format(self.ip))

                if response.status_code != 200:
                    continue

                data = json.decode(response.text)

                for item in data["rdata"]:
                    self.signal.emit(item["port"], item["value"])

                time.sleep(self.timebase)

        except BaseException as e:
            print(str(e))

    def adjustTimebase(self, time):
        self.timebase = time

    def stop(self):
        self.running = False



