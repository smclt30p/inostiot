# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QGraph(object):
    def setupUi(self, QGraph):
        QGraph.setObjectName("QGraph")
        QGraph.resize(675, 349)
        self.gridLayout = QtWidgets.QGridLayout(QGraph)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.graphContainer = QtWidgets.QWidget(QGraph)
        self.graphContainer.setObjectName("graphContainer")
        self.gridLayout.addWidget(self.graphContainer, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(25, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)

        self.retranslateUi(QGraph)
        QtCore.QMetaObject.connectSlotsByName(QGraph)

    def retranslateUi(self, QGraph):
        _translate = QtCore.QCoreApplication.translate
        QGraph.setWindowTitle(_translate("QGraph", "Form"))

