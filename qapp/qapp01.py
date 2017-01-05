# coding=utf-8
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal
from .mainwindow01 import MainWindow
from .gramodel import GraModel


class QApp(QApplication):

    modelChanged = pyqtSignal()

    def __init__(self, argv, frontend):
        super(QApp, self).__init__(argv)
        self.frontEnd = frontend
        self.initGraphEvent()
        self.mainwindow = MainWindow()

    # event handlers
    def initGraphEvent(self):
        # self.frontEnd.setRedrawState(state)
        # self.frontEnd.setGraphName(name)
        # self.frontEnd.setDirected(directed)
        # self.frontEnd.setNodesDefaultShape('circle')
        self.frontEnd.loadGraph()

    def addChildNodeEvent(self, parent):
        self.frontEnd.addChildNode(parent)
        # emit model changed
        self.modelChanged.emit()

    def deleteLeafNode(self, label):
        reGraph = False
        self.dbms.deleteLeafNode(label, forceReGraph=reGraph)

    # datafeeds for widgets
    def sceneWidgetData(self):
        return self.frontEnd.graph, self.frontEnd.boundingBox

    def t_dataWidgetData(self, row, column):
        return self.frontEnd.t_dataData(row, column)

    def t_dataDimension(self, whichDimension):
        return self.frontEnd.t_dataDimension(whichDimension)