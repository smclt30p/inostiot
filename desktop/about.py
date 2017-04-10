from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from desktop.Ui_AboutDialog import Ui_AboutDialog


class About(QDialog):

    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon("desktop\icon.png"))
        self.ui.bg.setPixmap(QPixmap("desktop\logo.png"))
        self.ui.version_string.setText("1.0")
