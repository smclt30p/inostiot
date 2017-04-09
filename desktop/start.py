import traceback

import demjson
import requests
from PyQt5.QtCore import QThread, pyqtSignal, Q_FLAGS
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QMessageBox

from desktop.MainWindow import MainWindow
from desktop.Ui_Start import Ui_StartDialog
from desktop.settings import Settings


class Start(QDialog):

    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.ui = Ui_StartDialog()
        self.ui.setupUi(self)
        self.ui.logo.setPixmap(QPixmap("desktop/banner.png"))
        self.setWindowTitle("InostIOT Starter")
        self.setWindowIcon(QIcon("icon.png"))

        self.ui.connectbtn.clicked.connect(self.startInostIOT)

        self.worker = StartWorker()
        self.worker.failed.connect(self.failed)
        self.worker.ok.connect(self.startMain)

        self.settings = Settings()

        ip = self.settings.read("old_ip")
        if ip is not None:
            self.ip = ip
            self.ui.server.setText(self.ip)

    def startMain(self, ip):

        try:

            self.settings.write("old_ip", ip)
            self.window = MainWindow(ip, flags=Q_FLAGS())
            self.window.show()
            self.close()

        except BaseException as e:
            traceback.print_exc()

    def startInostIOT(self):

        ip = self.ui.server.text()

        if len(ip) == 0:
            QMessageBox.critical(self, "Error", "No IP address provided! Please input the ArdADC server IP!")
            return

        self.ui.connectbtn.setEnabled(False)
        self.ui.server.setEnabled(False)
        self.ui.adclabel.setEnabled(False)
        self.worker.setIp(ip)
        self.worker.start()

    def failed(self, data):
        QMessageBox.critical(self, "Error", data)
        self.ui.connectbtn.setEnabled(True)
        self.ui.server.setEnabled(True)
        self.ui.adclabel.setEnabled(True)

class StartWorker(QThread):

    failed = pyqtSignal(str)
    ok = pyqtSignal(str)

    def setIp(self, ip):
        self.ip = ip

    def run(self):

        try:
            response = requests.get("http://{}/api?version".format(self.ip))
            if response.status_code != 200:
                raise BaseException("Non-valid HTTP code!")
            json = demjson.JSON()
            data = json.decode(response.text)
            if data["status"] != "OK":
                raise BaseException("Server returned non-OK!")
            self.ok.emit(self.ip)
        except BaseException as e:
            traceback.print_exc()
            self.failed.emit(str(e))
