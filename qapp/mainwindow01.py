# coding=utf-8
from PyQt5.QtWidgets import (QMainWindow, QFrame, QHBoxLayout, QGraphicsView,
                             QSizePolicy, QTableView)
from PyQt5.QtCore import QSize, QCoreApplication
from .grascene import GraScene
# from .gramodel import GraModel


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app = QCoreApplication.instance()
        self.setWindowTitle('Basic Drawing')
        cf = QFrame()
        self.setCentralWidget(cf)
        cf.setFrameStyle(QFrame.Box | QFrame.Plain)
        mainLayout = QHBoxLayout()
        cf.setLayout(mainLayout)
        self.sc = GraScene()
        westFrame = graWidget(self.sc)
        eastFrame = QFrame()
        eastFrame.setFrameStyle(QFrame.Box | QFrame.Plain)
        mainLayout.addWidget(westFrame)
        mainLayout.addWidget(eastFrame)
        eastLayout = QHBoxLayout()
        eastFrame.setLayout(eastLayout)
        self.dataView = QTableView()
        self.dataView.verticalHeader().hide()
        self.pathView = QTableView()
        # dataView.setModel(GraModel(self.app.dbms.listDataTable))
        eastLayout.addWidget(self.dataView)
        eastLayout.addWidget(self.pathView)


class graWidget(QGraphicsView):
    def __init__(self, parent=None):
        super(graWidget, self).__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def sizeHint(self):
        return QSize(600, 540)
