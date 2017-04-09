# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(792, 452)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.sensor_view = QtWidgets.QWidget()
        self.sensor_view.setObjectName("sensor_view")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.sensor_view)
        self.gridLayout_2.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.status_box = QtWidgets.QGroupBox(self.sensor_view)
        self.status_box.setObjectName("status_box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.status_box)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frequency_label = QtWidgets.QLabel(self.status_box)
        self.frequency_label.setObjectName("frequency_label")
        self.verticalLayout_2.addWidget(self.frequency_label)
        self.frequency_spinner = QtWidgets.QDoubleSpinBox(self.status_box)
        self.frequency_spinner.setSingleStep(0.001)
        self.frequency_spinner.setObjectName("frequency_spinner")
        self.verticalLayout_2.addWidget(self.frequency_spinner)
        self.resolution_label = QtWidgets.QLabel(self.status_box)
        self.resolution_label.setObjectName("resolution_label")
        self.verticalLayout_2.addWidget(self.resolution_label)
        self.resolution_spinbox = QtWidgets.QSpinBox(self.status_box)
        self.resolution_spinbox.setObjectName("resolution_spinbox")
        self.verticalLayout_2.addWidget(self.resolution_spinbox)
        self.gridLayout_2.addWidget(self.status_box, 2, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.sensor_view)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.upper_dial = QtWidgets.QDial(self.groupBox)
        self.upper_dial.setMinimumSize(QtCore.QSize(50, 50))
        self.upper_dial.setMaximumSize(QtCore.QSize(50, 50))
        self.upper_dial.setMaximum(1023)
        self.upper_dial.setObjectName("upper_dial")
        self.gridLayout.addWidget(self.upper_dial, 1, 0, 1, 1)
        self.lower_dial = QtWidgets.QDial(self.groupBox)
        self.lower_dial.setMinimumSize(QtCore.QSize(50, 50))
        self.lower_dial.setMaximumSize(QtCore.QSize(50, 50))
        self.lower_dial.setMaximum(1023)
        self.lower_dial.setObjectName("lower_dial")
        self.gridLayout.addWidget(self.lower_dial, 1, 2, 1, 1)
        self.upper_label = QtWidgets.QLabel(self.groupBox)
        self.upper_label.setAlignment(QtCore.Qt.AlignCenter)
        self.upper_label.setObjectName("upper_label")
        self.gridLayout.addWidget(self.upper_label, 2, 0, 1, 1)
        self.lower_label = QtWidgets.QLabel(self.groupBox)
        self.lower_label.setAlignment(QtCore.Qt.AlignCenter)
        self.lower_label.setObjectName("lower_label")
        self.gridLayout.addWidget(self.lower_label, 2, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(47, 12, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.sensor_view)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)
        self.graph_container = QtWidgets.QWidget(self.sensor_view)
        self.graph_container.setObjectName("graph_container")
        self.gridLayout_2.addWidget(self.graph_container, 0, 1, 4, 1)
        self.gridLayout_2.setColumnStretch(0, 10)
        self.gridLayout_2.setColumnStretch(1, 90)
        self.tabWidget.addTab(self.sensor_view, "")
        self.logger_tab = QtWidgets.QWidget()
        self.logger_tab.setObjectName("logger_tab")
        self.tabWidget.addTab(self.logger_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.sensor_list = QtWidgets.QTreeWidget(self.centralwidget)
        self.sensor_list.setObjectName("sensor_list")
        self.verticalLayout.addWidget(self.sensor_list)
        self.verticalLayout.setStretch(0, 70)
        self.verticalLayout.setStretch(1, 30)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 792, 21))
        self.menubar.setObjectName("menubar")
        self.menuProperties = QtWidgets.QMenu(self.menubar)
        self.menuProperties.setObjectName("menuProperties")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionAbout_InostIOT = QtWidgets.QAction(MainWindow)
        self.actionAbout_InostIOT.setObjectName("actionAbout_InostIOT")
        self.menuProperties.addAction(self.actionSettings)
        self.menuAbout.addAction(self.actionAbout_InostIOT)
        self.menubar.addAction(self.menuProperties.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.status_box.setTitle(_translate("MainWindow", "Settings"))
        self.frequency_label.setText(_translate("MainWindow", "Time base (s)"))
        self.resolution_label.setText(_translate("MainWindow", "Resolution (samples)"))
        self.groupBox.setTitle(_translate("MainWindow", "Levels"))
        self.upper_label.setText(_translate("MainWindow", "Upper"))
        self.lower_label.setText(_translate("MainWindow", "Lower"))
        self.checkBox.setText(_translate("MainWindow", "Sensor enabled"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sensor_view), _translate("MainWindow", "Sensor View"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logger_tab), _translate("MainWindow", "Logger"))
        self.sensor_list.headerItem().setText(0, _translate("MainWindow", "Sensor"))
        self.sensor_list.headerItem().setText(1, _translate("MainWindow", "Source"))
        self.sensor_list.headerItem().setText(2, _translate("MainWindow", "Range"))
        self.sensor_list.headerItem().setText(3, _translate("MainWindow", "Color"))
        self.menuProperties.setTitle(_translate("MainWindow", "Properties"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionAbout_InostIOT.setText(_translate("MainWindow", "About InostIOT"))

