import csv

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog


class Logger(QObject):

    logging = False

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def openFile(self):

        self.ui.logger_enable.setEnabled(False)

        if not self.ui.logger_enable.isChecked():
            return

        self.path = QFileDialog.getSaveFileName(filter="CSV file (*.csv)")[0]

        if len(self.path) == 0:
            return

        self.file = open(self.path, "w+", newline="")
        self.writer = csv.writer(self.file, delimiter=";")
        self.logging = True

    def writeValues(self, data):
        if not self.logging: return
        self.writer.writerow(data)

    def close(self):
        self.ui.logger_enable.setEnabled(True)
        if not self.logging: return
        self.logging = False
        self.file.close()