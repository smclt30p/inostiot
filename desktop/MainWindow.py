import demjson
import requests
from PyQt5.QtCore import QThread, pyqtSignal, Q_FLAGS
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QTreeWidgetItem
import time
from desktop.Ui_MainWindow import Ui_MainWindow
from desktop.about import About
from desktop.graph.builder import Builder
from desktop.graphworker import GraphWorker
from desktop.settings import Settings


class MainWindow(QMainWindow):

    workerRunning = False
    upperLimit = 0
    lowerLimit = 0

    def __init__(self,ip, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.ip = ip

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("InostIOT")
        self.setWindowIcon(QIcon("icon.png"))

        self.layout = QHBoxLayout(self.ui.graph_container)

        self.graph = Builder() \
            .setResolution(60) \
            .setRange(1024) \
            .setGridRows(12) \
            .setAxisMax(5.0) \
            .setRefreshStep(0.5) \
            .setUnit("V") \
            .build()

        self.settings = Settings.getInstance()
        upper = self.settings.read("upper_val")
        lower = self.settings.read("lower_val")

        if upper is not None:
            self.upperLimit = upper
        if lower is not None:
            self.lowerLimit = lower

        self.ui.lower_dial.sliderMoved.connect(self.adjustLower)
        self.ui.upper_dial.sliderMoved.connect(self.adjustUpper)

        self.ui.upper_dial.setValue(int(self.upperLimit))
        self.ui.lower_dial.setValue(int(self.lowerLimit))
        self.graph.adjustUpper(int(self.upperLimit))
        self.graph.adjustLower(int(self.lowerLimit))

        self.ui.resolution_spinbox.setValue(self.graph.resolution())
        self.ui.resolution_spinbox.valueChanged.connect(self.graph.adjustResolution)

        self.ui.frequency_spinner.setValue(self.graph.frequency())
        self.ui.frequency_spinner.valueChanged.connect(self.graph.adjustFrequency)

        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.graph)

        self.ui.actionAbout_InostIOT.triggered.connect(self.openAbout)
        self.ui.monitor_start.clicked.connect(self.toggleMonitor)

        self.addSensors()

    def adjustUpper(self, int):
        self.graph.adjustUpper(int)
        self.settings.write("upper_val", int)

    def adjustLower(self, int):
        self.graph.adjustLower(int)
        self.settings.write("lower_val", int)

    def addSensors(self):

        for i in range(0, 6):
            item = QTreeWidgetItem()
            item.setText(0, "Sensor {}".format(i))
            item.setText(1, "Active")
            item.setText(2, "ArdADC")
            item.setText(3, "1024")
            item.setText(4, "#FF0000")
            self.ui.sensor_list.addTopLevelItem(item)

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
            self.ui.frequency_spinner.valueChanged.connect(self.worker.adjustTimebase)
            self.worker.start()


    def openAbout(self):
        self.about = About(flags=Q_FLAGS())
        self.about.show()