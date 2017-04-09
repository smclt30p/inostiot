import sys
import time

import demjson
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget

from desktop.graph import QGraph


def main():

    app = QApplication(sys.argv)

    main = QWidget()
    main.resize(700, 300)

    graph = QGraph.Builder(main) \
        .setResolution(60)\
        .setRange(1024)\
        .setGridRows(12) \
        .setAxisMax(5.0) \
        .setRefreshStep(0.5)\
        .setUnit("V")\
        .build()

    worker = GraphWorker(graph)
    worker.signal.connect(graph.appendData)
    worker.start()

    graph.setWindowTitle("ADC")
    graph.setMinimumSize(300, 50)

    main.show()

    exit(app.exec_())


class GraphWorker(QThread):

    signal = pyqtSignal(int, float)

    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.graph.addDataset("#FF0000")
        self.graph.addDataset("#00FF00")
        self.graph.addDataset("#0000FF")
        self.graph.addDataset("#FFFF00")
        self.graph.addDataset("#FF00FF")
        self.graph.addDataset("#00FFFF")

    def run(self):

        json = demjson.JSON()

        try:
            while True:

                response = requests.get("http://192.168.1.109/api?port=0,1,2,3,4,5")

                if response.status_code != 200:
                    continue

                data = json.decode(response.text)

                for item in data["rdata"]:
                    self.signal.emit(item["port"], item["value"])

                time.sleep(0.5)

        except BaseException as e:
            print(str(e))



if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Missing port argument! COMX for Windows, /dev/xxx for POSIX")
        exit(-1)

    main()