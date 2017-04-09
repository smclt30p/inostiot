import demjson
import requests
from PyQt5.QtCore import QThread, pyqtSignal, Q_FLAGS
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout
import time
from desktop.Ui_MainWindow import Ui_MainWindow
from desktop.about import About
from desktop.graph import QGraph


class MainWindow(QMainWindow):

    workerRunning = False

    def __init__(self,ip, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.ip = ip

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("InostIOT")
        self.setWindowIcon(QIcon("icon.png"))

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

        self.ui.actionAbout_InostIOT.triggered.connect(self.openAbout)

        self.ui.monitor_start.clicked.connect(self.toggleMonitor)

    def toggleMonitor(self):

        if self.workerRunning:
            self.ui.monitor_start.setText("Start monitor")
            self.workerRunning = False
            self.worker.stop()
            self.graph.clear()
        else:
            self.workerRunning = True
            self.ui.monitor_start.setText("Stop monitor")
            self.worker = GraphWorker(self.ip, self.graph, self.graph.frequency())
            self.worker.signal.connect(self.graph.appendData)
            self.ui.frequency_spinner.valueChanged.connect(self.worker.adjustTimebase)
            self.worker.start()


    def openAbout(self):

        self.about = About(flags=Q_FLAGS())
        self.about.show()

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

