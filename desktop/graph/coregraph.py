import traceback

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPen, QColor, QStaticText, QLinearGradient, QPainter
from PyQt5.QtWidgets import QWidget

from desktop.dataset import DataSet


class CoreGraph(QWidget):
    upper = 0
    lower = 0
    gridRows = 10
    gridColumns = 10
    graphdata = []
    currID = 0
    range = -1
    resolution = -1
    dynamicRange = True
    dynamicResolution = True
    walking = False

    def drawLimit(self, painter, value, color, text):

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

                if (len(dataset)) == 0: return

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

                if len(data["data"]) == 0:
                    return

                color = QColor(data["color"])
                pen.setColor(color)
                painter.setPen(pen)
                renderDataSet(self, data["data"])

            if self.upper != 0:
                self.drawLimit(painter, self.upper, "#FF0000", "UPPER")

            if self.lower != 0:
                self.drawLimit(painter, self.lower, "#00FF00", "LOWER")

        except BaseException:
            traceback.print_exc()

    def addData(self, data):
        self.graphdata.append(data)

    def addDataset(self, color):

        set = DataSet()
        set.setMax(self.resolution + 1)

        for i in range(0, self.resolution):
            set.append(-1)

        self.graphdata.append({"id": self.currID, "color": color,
                               "data": set})

        if self.dynamicRange:
            self.range = self.maxInAllData()

        if self.dynamicResolution:
            self.resolution = self.longestInAllData() - 1

        self.currID += 1
        return self.currID - 1

    def appendData(self, datasetId, data):
        for item in self.graphdata:
            if item["id"] == datasetId:
                item["data"].append(data)

        self.repaint()

    def maxInAllData(self):
        maxFound = -1
        i = 0
        for item in self.graphdata:
            test = self.maxWithDynamicFactor(item["data"])
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
            test = len(item["data"])
            if test > maxFound:
                maxFound = test
        return maxFound

    def clear(self):
        self.currID = 0
        self.graphdata.clear()
        self.repaint()