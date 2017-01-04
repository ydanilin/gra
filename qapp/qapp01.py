# coding=utf-8
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from .mainwindow01 import MainWindow
from .gramodel import GraModel


class QApp(QApplication):
    def __init__(self, argv, frontend):
        super(QApp, self).__init__(argv)
        self.frontEnd = frontend
        self.initGraphEvent()
        self.mainwindow = MainWindow()

    def initGraphEvent(self):
        # self.frontEnd.setRedrawState(state)
        # self.frontEnd.setGraphName(name)
        # self.frontEnd.setDirected(directed)
        # self.frontEnd.setNodesDefaultShape('circle')
        self.frontEnd.loadGraph()

    def sceneWidgetData(self):
        return self.frontEnd.graph, self.frontEnd.boundingBox

    def addChildNode(self, parentLabel):
        # will take this parameter somewhere in the settings
        reGraph = False
        self.dbms.addChildNode(parentLabel, forceReGraph=reGraph)

    def deleteLeafNode(self, label):
        reGraph = False
        self.dbms.deleteLeafNode(label, forceReGraph=reGraph)

    def t_dataWidgetData(self, row, column):
        return self.frontEnd.t_dataData(row, column)

    def t_dataDimension(self, whichDimension):
        return self.frontEnd.t_dataDimension(whichDimension)