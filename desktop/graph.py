import traceback

import collections
from PyQt5.QtCore import QRect, Q_FLAGS
from PyQt5.QtGui import QLinearGradient, QPainter, QColor, QPen, QStaticText
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets

class QGraph(QWidget):

    axisMax = 0
    unit = ""
    refreshStep = 0

    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        self.setupUi()

    def setGraph(self, graph):
        self.graph = graph
        self.graphLayout.addWidget(graph)

    def setupUi(self):

        self.resize(700, 250)
        self.gridLayout = QtWidgets.QGridLayout(self)

        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        spacerItem1 = QtWidgets.QSpacerItem(25, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)


        self.graphContainer = QtWidgets.QWidget(self)
        self.graphLayout = QtWidgets.QHBoxLayout(self.graphContainer)

        self.gridLayout.addWidget(self.graphContainer, 0, 1, 1, 1)
        self.graphLayout.setContentsMargins(0, 0, 0, 0)

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)

        try:

            painter = QPainter(self)
            rowStep = self.graph.height() / self.graph.gridRows
            axisStep = self.axisMax / self.graph.gridRows
            axisCurr = self.axisMax
            currPos = 6

            for i in range(0, self.graph.gridRows + 1):
                painter.drawStaticText(10, currPos, QStaticText(str(round(axisCurr,1)) + self.unit))
                currPos += rowStep
                axisCurr -= axisStep

            sps = 1 / self.refreshStep
            painter.drawStaticText(50, self.graph.height() + 20, QStaticText(str(sps) + " Hz"))
            painter.drawStaticText(120, self.graph.height() + 20, QStaticText(str(self.refreshStep) + " s/div"))


        except BaseException:
            traceback.print_exc()

    class Builder:

        def __init__(self):
            self.subject = QGraph(flags=Q_FLAGS())
            self.graph = QGraph.CoreGraph()
            self.subject.setGraph(self.graph)

        def setDynamicRange(self, bool):
            self.subject.graph.dynamicRange = bool
            return self

        def setDynamicResolution(self, bool):
            self.subject.graph.dynamicResolution = bool
            return self

        def setGridRows(self, count):
            self.subject.graph.gridRows = count
            return self

        def setResolution(self, count):
            self.subject.graph.dynamicResolution = False
            self.subject.graph.resolution = count - 1
            self.subject.graph.gridColumns = count
            return self

        def setRange(self, count):
            self.subject.graph.dynamicRange = False
            self.subject.graph.range = count
            return self

        def setWalking(self, boo):
            self.subject.graph.walking = boo
            return self

        def setAxisMax(self, max):
            self.subject.axisMax = max
            return self

        def setUnit(self, unit):
            self.subject.unit = unit
            return self

        def setRefreshStep(self, step):
            self.subject.refreshStep = step
            return self

        def build(self):
            return self.subject

    def appendData(self, id, data):
        self.graph.appendData(id, data)

    def addDataset(self ,color):
        return self.graph.addDataset(color)

    def adjustUpdateSpeed(self, speed):
        self.refreshStep = speed

    class CoreGraph(QWidget):

        gridRows = 10
        gridColumns = 10
        graphdata = []
        currID = 0
        range = -1
        resolution = -1
        dynamicRange = True
        dynamicResolution = True
        walking = False
        

        def drawLimit(self,painter, value, color, text):

            oldPen = painter.pen()
            pen = QPen()
            color = QColor(color)
            pen.setColor(color)
            painter.setPen(pen)
            y = self.height() - ((value / self.range) * self.height())

            painter.drawLine(0, y, self.width(), y)
            painter.drawStaticText(5, y - 15, QStaticText(text))
            painter.setPen(oldPen)

        def paintEvent(self, QPaintEvent):

            try:

                width = self.width()
                height = self.height()

                black = QColor("#000000")
                gray = QColor("#303030")

                area = QRect(0, 0, width, height)

                width = area.width()
                height = area.height()

                gradient = QLinearGradient(width, 0, width, height)
                gradient.setColorAt(0, black)
                gradient.setColorAt(1, gray)

                painter = QPainter(self)
                painter.drawRect(area)
                painter.fillRect(area, gradient)

                red = QColor("#3a3a3a")

                pen = QPen()
                pen.setColor(red)
                painter.setPen(pen)

                painterX = 0
                painterY = 0
                vertSpit = 0
                horizontalSplit = 0

                if self.gridRows != 0 and self.gridColumns != 0:
                    vertSpit = height / self.gridRows
                    horizontalSplit = width / self.gridColumns

                for i in range(0, self.gridRows):
                    painter.drawLine(painterX, painterY, width, painterY)
                    painterY = painterY + vertSpit

                painterX = 0
                painterY = 0

                for i in range(0, self.gridColumns):
                    painter.drawLine(painterX, painterY, painterX, height)
                    painterX = painterX + horizontalSplit

                def renderDataSet(self, dataset):

                    painter.setRenderHint(QPainter.Antialiasing, True)
                    initial = True
                    startX = 0
                    startY = (self.range - dataset[0]) / self.range * height
                    endX = 0
                    endY = 0
                    rendered = 0

                    for item in dataset:

                        if rendered > self.resolution:
                            break

                        if initial:
                            endY = (self.range - item) / self.range * height
                            painter.drawLine(startX, startY, endX, endY)
                            initial = False
                        else:
                            startX = endX
                            startY = endY
                            endX = startX + (width / self.resolution)
                            endY = (self.range - item) / self.range * height
                            painter.drawLine(startX, startY, endX, endY)

                        rendered += 1


                for data in self.graphdata:

                    if len(list(data["data"])) == 0:
                        return

                    color = QColor(data["color"])
                    pen.setColor(color)
                    painter.setPen(pen)
                    renderDataSet(self, list(data["data"]))


                self.drawLimit(painter, 768, "#FF0000", "DANGER")
                self.drawLimit(painter, 166, "#00FF00", "OK")

            except BaseException:
                traceback.print_exc()

        def addDataset(self, color):

            set = collections.deque(maxlen=self.resolution + 1)
            for i in range(0, self.resolution):
                set.append(-1)

            self.graphdata.append({"id": self.currID ,"color":color,
                                   "data":set})

            if self.dynamicRange:
                self.range = self.maxInAllData()

            if self.dynamicResolution:
                self.resolution = self.longestInAllData() - 1

            self.currID += 1
            return self.currID -1

        def appendData(self, datasetId, data):
            for item in self.graphdata:
                if item["id"] == datasetId:
                    item["data"].append(data)

            self.repaint()

        def maxInAllData(self):
            maxFound = -1
            i = 0
            for item in self.graphdata:
                test = self.maxWithDynamicFactor(list(item["data"]))
                if test > maxFound:
                    maxFound = test
                i += 1
            return maxFound

        def maxWithDynamicFactor(self, array):
            maxFound = 0
            i = 0
            for item in array:
                if i > self.resolution:
                    break
                if item > maxFound:
                    maxFound = item
                i += 1
            return maxFound

        def longestInAllData(self):
            maxFound = 0
            for item in self.graphdata:
                test = len(list(item["data"]))
                if test > maxFound:
                    maxFound = test
            return maxFound

        def clear(self):
            self.graphdata = []
            self.repaint()
