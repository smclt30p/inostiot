import demjson
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout
import time
from desktop.Ui_MainWindow import Ui_MainWindow
from desktop.graph import QGraph


class MainWindow(QMainWindow):

    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.layout = QHBoxLayout(self.ui.graph_container)

        self.graph = QGraph.Builder() \
            .setResolution(60) \
            .setRange(1024) \
            .setGridRows(12) \
            .setAxisMax(5.0) \
            .setRefreshStep(0.5) \
            .setUnit("V") \
            .build()

        self.ui.lower_dial.sliderMoved.connect(self.graph.adjustLower)
        self.ui.upper_dial.sliderMoved.connect(self.graph.adjustUpper)

        self.ui.resolution_spinbox.setValue(self.graph.resolution())
        self.ui.resolution_spinbox.valueChanged.connect(self.graph.adjustResolution)

        self.ui.frequency_spinner.setValue(self.graph.frequency())
        self.ui.frequency_spinner.valueChanged.connect(self.graph.adjustFrequency)

        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.graph)

        self.worker = GraphWorker(self.graph, self.graph.frequency())
        self.worker.signal.connect(self.graph.appendData)
        self.ui.frequency_spinner.valueChanged.connect(self.worker.adjustTimebase)
        self.worker.start()

class GraphWorker(QThread):

    signal = pyqtSignal(int, float)
    timebase = 1

    def __init__(self, graph, initial):
        super().__init__()

        self.timebase = initial

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
            while True:

                response = requests.get("http://192.168.1.109/api?port=0,1,2,3,4,5")

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

