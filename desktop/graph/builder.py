from desktop.graph.coregraph import CoreGraph
from desktop.graph.graph import QGraph


class Builder:

    def __init__(self):
        self.subject = QGraph()
        self.graph = CoreGraph()
        self.subject.setGraph(self.graph)

    def setDynamicRange(self, bool):
        self.subject.graph.dynamicRange = bool
        return self

    def setDynamicResolution(self, bool):
        self.subject.graph.dynamicResolution = bool
        return self

    def setGridRows(self, count):
        self.subject.graph.gridRows = count
        return self

    def setResolution(self, count):
        self.subject.graph.dynamicResolution = False
        self.subject.graph.resolution = count - 1
        self.subject.graph.gridColumns = count
        return self

    def setRange(self, count):
        self.subject.graph.dynamicRange = False
        self.subject.graph.range = count
        return self

    def setWalking(self, boo):
        self.subject.graph.walking = boo
        return self

    def setAxisMax(self, max):
        self.subject.axisMax = max
        return self

    def setUnit(self, unit):
        self.subject.unit = unit
        return self

    def setRefreshStep(self, step):
        self.subject.refreshStep = step
        return self

    def build(self):
        return self.subject