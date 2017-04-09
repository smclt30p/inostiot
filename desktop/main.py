import sys

from PyQt5.QtCore import Q_FLAGS
from PyQt5.QtWidgets import QApplication

from desktop.MainWindow import MainWindow
from desktop.start import Start


def main():

    app = QApplication(sys.argv)

    window = Start(flags=Q_FLAGS())
    window.show()

    exit(app.exec_())

if __name__=="__main__":
    main()