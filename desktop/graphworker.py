import demjson
import requests
import time
from PyQt5.QtCore import QThread, pyqtSignal

from desktop.dataset import DataSet, Sensor


class GraphWorker(QThread):

    repaint = pyqtSignal(list)

    toggleSensor = pyqtSignal(int)
    changeSensorColor = pyqtSignal(str)

    timebase = 1
    running = True
    graphdata = []


    def appendData(self, port, data):
        for item in self.graphdata:
            if item["port"] == port:
                item["data"].append(data)

    def __init__(self,ip, graph, sensors):
        super().__init__()

        self.sensors = sensors
        self.timebase = graph.frequency()
        self.ip = ip
        self.graph = graph
        self.repaint.connect(self.graph.repaintData)


    def start(self):

        for sensor in self.sensors:
            self.graphdata.append({"port": sensor.port, "color": sensor.color,
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

                for i in range(0, len(self.graphdata)):

                    if self.sensors[i].active:
                        self.graphdata[i]["color"] = self.sensors[i].color
                        queue.append(self.graphdata[i])

                self.repaint.emit(queue)
                time.sleep(self.timebase)

        except BaseException as e:
            print(str(e))

    def adjustTimebase(self, time):
        self.timebase = time

    def stop(self):
        self.graphdata.clear()
        self.running = False



