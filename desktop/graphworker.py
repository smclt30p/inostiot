import demjson
import requests
import time
from PyQt5.QtCore import QThread, pyqtSignal

from desktop.dataset import DataSet, Sensor


class GraphWorker(QThread):

    repaint = pyqtSignal(list)
    timebase = 1
    running = True
    sensors = []
    graphdata = []


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

        for i in range(0, 6):

            sensor = Sensor()
            sensor.id = i
            sensor.color = "#FFFFFF"
            sensor.data = DataSet()
            sensor.data.setMax(self.graph.resolution() + 1)

            for i in range(0, self.graph.resolution()):
                sensor.data.append(-1)

            self.sensors.append(sensor)

    def start(self):

        for sensor in self.sensors:
            self.graphdata.append({"id": sensor.id, "color": sensor.color,
                                   "data": sensor.data})

        self.running = True
        super().start()

    def run(self):

        json = demjson.JSON()
        queue = []

        try:
            while self.running:

                response = requests.get("http://{}/api?port=0,1,2,3,4,5".format(self.ip))

                if response.status_code != 200:
                    continue

                data = json.decode(response.text)

                for item in data["rdata"]:
                    self.appendData(item["port"], item["value"])

                queue.clear()

                for item in self.graphdata:
                    if int(item["id"]) == 1:
                        item["color"] = "#FFFFFF"
                    queue.append(item)

                self.repaint.emit(queue)
                time.sleep(self.timebase)

        except BaseException as e:
            print(str(e))

    def adjustTimebase(self, time):
        self.timebase = time

    def stop(self):
        self.graphdata.clear()
        self.running = False



