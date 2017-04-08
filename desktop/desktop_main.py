import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication

from core.ardadc import ArdADC
from desktop.graph import QGraph


def main():

    app = QApplication(sys.argv)

    graph = QGraph.Builder() \
        .setResolution(120)\
        .setRange(1024)\
        .setGridRows(15) \
        .setAxisMax(5.0) \
        .setRefreshStep(0.016)\
        .setUnit("V")\
        .build()

    worker = GraphWorker(graph)
    worker.signal.connect(graph.appendData)
    worker.start()

    graph.setWindowTitle("ADC")
    graph.setMinimumSize(300, 50)
    graph.show()

    exit(app.exec_())


class GraphWorker(QThread):

    adc = ArdADC(sys.argv[1])
    adc.handshake()

    signal = pyqtSignal(int, float)

    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.id = self.graph.addDataset("#FF0000")
        self.id2 = self.graph.addDataset("#00FF00")
        self.id3 = self.graph.addDataset("#0000FF")

    def run(self):

        try:
            while True:
                self.signal.emit(self.id, self.adc.analog_read(0))
                self.signal.emit(self.id2, self.adc.analog_read(1))
                self.signal.emit(self.id3, self.adc.analog_read(3))
                time.sleep(0.016)
        except BaseException as e:
            print(str(e))



if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Missing port argument! COMX for Windows, /dev/xxx for POSIX")
        exit(-1)

    main()