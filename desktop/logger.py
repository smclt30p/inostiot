import csv
import datetime

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog, QTreeWidgetItem

from desktop.settings import Settings


class Logger(QObject):

    logging = False

    def __init__(self, ui):
        super().__init__()

        self.ui = ui
        self.settings = Settings()

        self.logs_time = self.settings.readList("log_time")
        self.logs_path = self.settings.readList("log_path")

        if self.logs_path is None or self.logs_time is None:
            return

        self.refreshList()

    def refreshList(self):

        self.ui.old_list.clear()

        if len(self.logs_path) == len(self.logs_time):
            for i in range(len(self.logs_path)):
                item = QTreeWidgetItem()
                item.setText(0, self.logs_time[i])
                item.setText(1, self.logs_path[i])
                self.ui.old_list.addTopLevelItem(item)

    def openFile(self):

        self.ui.logger_enable.setEnabled(False)

        if not self.ui.logger_enable.isChecked():
            return

        self.path = QFileDialog.getSaveFileName(filter="CSV file (*.csv)")[0]

        if len(self.path) == 0:
            return

        if self.logs_path is None or self.logs_time is None:
            self.logs_path = []
            self.logs_time = []

        self.logs_path.append(self.path)
        self.logs_time.append('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

        self.settings.writeList(self.logs_time, "log_time")
        self.settings.writeList(self.logs_path, "log_path")

        self.refreshList()

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