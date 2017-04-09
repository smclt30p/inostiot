import demjson
import requests
import time
from PyQt5.QtCore import QThread, pyqtSignal

from desktop.dataset import DataSet


class GraphWorker(QThread):

    repaint = pyqtSignal(list)
    timebase = 1
    running = True
    currID = 0
    graphdata = []

    def addDataset(self, color):

        set = DataSet()
        set.setMax(self.graph.resolution() + 1)

        for i in range(0, self.graph.resolution()):
            set.append(-1)

        self.graphdata.append({"id": self.currID, "color": color,
                               "data": set})

        self.currID += 1
        return self.currID - 1

    def appendData(self, datasetId, data):
        for item in self.graphdata:
            if item["id"] == datasetId:
                item["data"].append(data)

    def __init__(self,ip, graph, initial):
        super().__init__()

        self.timebase = initial
        self.ip = ip

        self.graph = graph
        self.repaint.connect(self.graph.repaintData)

        self.addDataset("#FF0000")
        self.addDataset("#00FF00")
        self.addDataset("#0000FF")
        self.addDataset("#FFFF00")
        self.addDataset("#FF00FF")
        self.addDataset("#00FFFF")

    def run(self):

        json = demjson.JSON()

        try:
            while self.running:

                response = requests.get("http://{}/api?port=0,1,2,3,4,5".format(self.ip))

                if response.status_code != 200:
                    continue

                data = json.decode(response.text)

                for item in data["rdata"]:
                    self.appendData(item["port"], item["value"])

                self.repaint.emit(self.graphdata)
                time.sleep(self.timebase)

        except BaseException as e:
            print(str(e))

    def adjustTimebase(self, time):
        self.timebase = time

    def stop(self):
        self.running = False



