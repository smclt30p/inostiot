import traceback

import collections
from PyQt5.QtCore import QRect, Q_FLAGS
from PyQt5.QtGui import QLinearGradient, QPainter, QColor, QPen, QStaticText
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets

from desktop.dataset import DataSet

class QGraph(QWidget):

    axisMax = 0
    unit = ""
    refreshStep = 0

    def clear(self):
        self.graph.clear()

    def setGraph(self, graph):
        self.setupUi()
        self.graph = graph
        self.graphLayout.addWidget(graph)


    def adjustUpper(self, upper):
        self.graph.upper = upper
        self.graph.repaint()

    def adjustLower(self, lower):
        self.graph.lower = lower
        self.graph.repaint()

    def adjustResolution(self, resolution):

        self.graph.resolution = resolution
        self.graph.gridColumns = resolution

        for set in self.graph.graphdata:
            set["data"].setMax(resolution)

        self.graph.repaint()

    def resolution(self):
        return self.graph.resolution

    def frequency(self):
        return self.refreshStep

    def adjustFrequency(self, freq):
        self.refreshStep = freq
        self.repaint()

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

            if self.refreshStep == 0: return
            sps = 1 / self.refreshStep
            painter.drawStaticText(50, self.graph.height() + 20, QStaticText(str(round(sps)) + " Hz"))
            painter.drawStaticText(120, self.graph.height() + 20, QStaticText(str(self.refreshStep) + " s/div"))


        except BaseException:
            traceback.print_exc()


    def adjustUpdateSpeed(self, speed):
        self.refreshStep = speed

    def repaintData(self, data):
        self.graph.repaintData(data)




