# coding=utf-8
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal
from .mainwindow01 import MainWindow
from .gramodel import GraModel


class QApp(QApplication):

    modelChanged = pyqtSignal()

    def __init__(self, argv, frontend):
        super(QApp, self).__init__(argv)
        self.frontEnd: object = frontend
        self.initGraphEvent()
        self.tDataTableModel = GraModel(self.t_dataWidgetData,
                                        self.t_dataDimension)
        # self.modelChanged.connect(self.puk)
        self.modelChanged.connect(lambda:
                                  self.tDataTableModel.layoutChanged.emit())

        self.mainwindow: object = MainWindow()
        self.modelChanged.emit()

    # event handlers
    def initGraphEvent(self):
        # self.frontEnd.setRedrawState(state)
        # self.frontEnd.setGraphName(name)
        # self.frontEnd.setDirected(directed)
        # self.frontEnd.setNodesDefaultShape('circle')
        self.frontEnd.loadGraph(True)

    def addChildNodeEvent(self, parent: int):
        self.frontEnd.addChildNode(parent)
        # emit model changed
        self.modelChanged.emit()

    def deleteLeafNodeEvent(self, label: int):
        self.frontEnd.deleteLeafNode(label)
        # emit model changed
        self.modelChanged.emit()

    # service functions for context menu events
    def hasChildren(self, label: int):
        return self.frontEnd.hasChildren(label)

    # datafeeds for widgets
    def sceneWidgetData(self):
        return self.frontEnd.graphData, self.frontEnd.graphData[0]['boundingBox']

    def t_dataWidgetData(self, row, column):
        return self.frontEnd.t_dataData(row, column)

    def t_dataDimension(self, whichDimension):
        return self.frontEnd.t_dataDimension(whichDimension)

    def t_pathWidgetData(self, row, column):
        return self.frontEnd.t_pathData(row, column)

    def t_pathDimension(self, whichDimension):
        return self.frontEnd.t_pathDimension(whichDimension)
