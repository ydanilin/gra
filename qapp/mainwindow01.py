# coding=utf-8
from PyQt5.QtWidgets import (QMainWindow, QFrame, QHBoxLayout, QGraphicsView,
                             QSizePolicy)
from PyQt5.QtCore import QSize
from .grascene import GraScene


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Basic Drawing')
        cf = QFrame()
        cf.setFrameStyle(QFrame.Box | QFrame.Plain)
        mainLayout = QHBoxLayout()
        self.sc = GraScene()
        westFrame = graWidget(self.sc)
        eastFrame = QFrame()
        eastFrame.setFrameStyle(QFrame.Box | QFrame.Plain)
        mainLayout.addWidget(westFrame)
        mainLayout.addWidget(eastFrame)
        cf.setLayout(mainLayout)
        self.setCentralWidget(cf)


class graWidget(QGraphicsView):
    def __init__(self, parent=None):
        super(graWidget, self).__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def sizeHint(self):
        return QSize(660, 540)
