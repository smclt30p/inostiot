# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\start.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StartDialog(object):
    def setupUi(self, StartDialog):
        StartDialog.setObjectName("StartDialog")
        StartDialog.resize(200, 142)
        StartDialog.setMinimumSize(QtCore.QSize(200, 0))
        StartDialog.setMaximumSize(QtCore.QSize(200, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(StartDialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.logo = QtWidgets.QLabel(StartDialog)
        self.logo.setMinimumSize(QtCore.QSize(200, 50))
        self.logo.setMaximumSize(QtCore.QSize(200, 50))
        self.logo.setObjectName("logo")
        self.verticalLayout.addWidget(self.logo)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setObjectName("gridLayout")
        self.server = QtWidgets.QLineEdit(StartDialog)
        self.server.setObjectName("server")
        self.gridLayout.addWidget(self.server, 1, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.connectbtn = QtWidgets.QPushButton(StartDialog)
        self.connectbtn.setObjectName("connectbtn")
        self.gridLayout.addWidget(self.connectbtn, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.adclabel = QtWidgets.QLabel(StartDialog)
        self.adclabel.setAlignment(QtCore.Qt.AlignCenter)
        self.adclabel.setObjectName("adclabel")
        self.gridLayout.addWidget(self.adclabel, 0, 0, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(StartDialog)
        QtCore.QMetaObject.connectSlotsByName(StartDialog)

    def retranslateUi(self, StartDialog):
        _translate = QtCore.QCoreApplication.translate
        StartDialog.setWindowTitle(_translate("StartDialog", "Dialog"))
        self.logo.setText(_translate("StartDialog", "logo"))
        self.connectbtn.setText(_translate("StartDialog", "Start"))
        self.adclabel.setText(_translate("StartDialog", "ArdADC Server"))

