import demjson
import requests
import time
from PyQt5.QtCore import QThread, pyqtSignal

from desktop.dataset import DataSet, Sensor
from desktop.logger import Logger


class GraphWorker(QThread):

    repaint = pyqtSignal(list)

    timebase = 1
    running = True
    graphdata = []


    def appendData(self, port, data):
        for item in self.graphdata:
            if item["port"] == port:
                item["data"].append(data)

    def __init__(self,ip, graph, sensors, ui):
        super().__init__()

        self.sensors = sensors
        self.timebase = graph.frequency()
        self.ip = ip
        self.graph = graph
        self.repaint.connect(self.graph.repaintData)
        self.ui = ui
        self.logger = Logger(self.ui)


    def start(self):

        self.logger.openFile()

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

                query = self.constructFromRunning()

                response = requests.get("http://{}/api?port={}".format(self.ip, query))

                if response.status_code != 200:
                    continue

                data = json.decode(response.text)
                datalog = []

                for item in data["rdata"]:
                    self.appendData(item["port"], item["value"])
                    datalog.append(item["value"])

                self.logger.writeValues(datalog)

                queue.clear()

                for i in range(0, len(self.graphdata)):

                    if self.sensors[i].active:
                        self.graphdata[i]["color"] = self.sensors[i].color
                        queue.append(self.graphdata[i])

                self.repaint.emit(queue)
                time.sleep(self.timebase)

        except BaseException as e:
            print(str(e))

    def constructFromRunning(self):

        query = ""

        for i in range(0, len(self.sensors)):
            if i == len(self.sensors) - 1:
                if (self.sensors[i].active):
                    query += "{}".format(self.sensors[i].port)
                break
            if (self.sensors[i].active):
                query += "{},".format(self.sensors[i].port)

        return query


    def adjustTimebase(self, time):
        self.timebase = time

    def stop(self):
        for item in self.sensors:
            for i in range(0, item.data.max):
                item.data.append(-1)
        self.graphdata.clear()
        self.logger.close()
        self.running = False


