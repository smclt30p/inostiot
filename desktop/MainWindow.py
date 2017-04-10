from PyQt5.QtCore import Q_FLAGS, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QTreeWidgetItem, QMenu

from desktop.Ui_MainWindow import Ui_MainWindow
from desktop.about import About
from desktop.dataset import Sensor, DataSet
from desktop.graph.builder import Builder
from desktop.graphworker import GraphWorker
from desktop.settings import Settings


class MainWindow(QMainWindow):

    workerRunning = False
    upperLimit = 0
    lowerLimit = 0
    sensors = []

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

        self.worker = GraphWorker(self.ip, self.graph, self.sensors)

        self.addSensors()

        self.ui.sensor_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.sensor_list.customContextMenuRequested.connect(self.contextMenuOpen)

        self.ui.sensor_list.itemChanged.connect(self.changeSensorColor)

    def changeSensorColor(self, item, pos):

        if not (self.isColor(item.text(4))):
            return

        item.sensor.color = item.text(4)

        colors = []

        for sensor in self.sensors:
            colors.append(sensor.color)

        self.settings.writeList(colors, "sensor_colors")

    def contextMenuOpen(self, pos):

        index = self.ui.sensor_list.indexAt(pos)
        menu = QMenu()

        action = menu.addAction("Toggle")
        action.index = index.row()
        action.triggered.connect(self.toggleSensorState)


        menu.exec(self.ui.sensor_list.mapToGlobal(pos))


    def toggleSensorState(self):
        i = self.sender().index
        self.sensors[i].active = not self.sensors[i].active

        toggled = []
        for sensor in self.sensors:
            toggled.append(sensor.active)

        self.settings.writeList(toggled, "sensors_toggled")

        self.refreshSensorList()

    def adjustUpper(self, int):
        self.graph.adjustUpper(int)
        self.settings.write("upper_val", int)

    def adjustLower(self, int):
        self.graph.adjustLower(int)
        self.settings.write("lower_val", int)

    def addSensors(self):

        for i in range(0, 6):

            sensor = Sensor()
            sensor.name = "Sensor {}".format(i)
            sensor.port = i
            sensor.color = "#FFFF00"
            sensor.data = DataSet()
            sensor.range = 1023
            sensor.data.setMax(self.graph.resolution() + 1)

            for i in range(0, self.graph.resolution()):
                sensor.data.append(-1)
            self.sensors.append(sensor)

        self.readsSensorStatesAndColorsFromDisk()
        self.refreshSensorList()

    def readsSensorStatesAndColorsFromDisk(self):

        toggled = self.settings.readList("sensors_toggled")
        colors = self.settings.readList("sensor_colors")

        if len(toggled) == len(self.sensors):
            for i in range(0, len(toggled)):
                self.sensors[i].active = bool(toggled[i])

        if len(colors) == len(self.sensors):
            for i in range(0, len(toggled)):
                self.sensors[i].color = colors[i]

    def refreshSensorList(self):

        self.ui.sensor_list.clear()

        for sensor in self.sensors:
            item = QTreeWidgetItem()
            item.setText(0, sensor.name)
            item.setText(1, str(sensor.active))
            item.setText(2, "ArdADC")
            item.setText(3, str(sensor.range))
            item.setText(4, sensor.color)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            item.sensor = sensor
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
            self.ui.frequency_spinner.valueChanged.connect(self.worker.adjustTimebase)
            self.worker.start()


    def openAbout(self):
        self.about = About(flags=Q_FLAGS())
        self.about.show()

    def isColor(self, color):

        if len(color) is not  7:
            return False

        if not color.startswith("#"):
            return False

        color = color.replace("#", "")

        try:
            int(color, 16)
            return True
        except ValueError:
            return False