# coding=utf-8
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from .mainwindow01 import MainWindow


class QApp(QApplication):
    def __init__(self, argv):
        super(QApp, self).__init__(argv)
        self.dbms = None
        self.mainwindow = MainWindow()

    def drawGraph(self, name='untitled'):
        self.dbms.loadGraph(name)

    def addChildNode(self, parentLabel):
        # will take this parameter somewhere in the settings
        reGraph = False
        self.dbms.addChildNode(parentLabel, forceReGraph=reGraph)

    def deleteLeafNode(self, label):
        reGraph = False
        self.dbms.deleteLeafNode(label, forceReGraph=reGraph)
