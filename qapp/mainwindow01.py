# coding=utf-8
from PyQt5.QtWidgets import (QMainWindow, QFrame, QHBoxLayout, QGraphicsView,
                             QSizePolicy, QTableView)
from PyQt5.QtCore import QSize, QCoreApplication
from .grascene import GraScene
from .gramodel import GraModel


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app:object = None
        self.dataView:object = None
        self.pathView:object = None

        self.app = QCoreApplication.instance()
        self.setWindowTitle('Basic Drawing')
        # central widget and main layout
        cf = QFrame()
        cf.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setCentralWidget(cf)
        mainLayout = QHBoxLayout()
        cf.setLayout(mainLayout)
        # graph scene and widget
        westFrame = graWidget(self.app)
        mainLayout.addWidget(westFrame)
        # right side
        eastFrame = QFrame()
        # eastFrame.setFrameStyle(QFrame.Box | QFrame.Plain)
        mainLayout.addWidget(eastFrame)
        eastLayout = QHBoxLayout()
        eastFrame.setLayout(eastLayout)
        # t_data table grid
        self.dataView = TDataTableGrid(self.app)
        eastLayout.addWidget(self.dataView)
        # t_path table grid
        self.pathView = TPathTableGrid(self.app)
        eastLayout.addWidget(self.pathView)


class graWidget(QGraphicsView):
    def __init__(self, app, parent=None):
        super(graWidget, self).__init__(parent)
        self.app: object = app
        self.setScene(GraScene())
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.app.doRedraw.connect(self.redraw)
        # self.scene().drawScene(self.app.sceneWidgetData())

    def redraw(self):
        self.scene().drawScene(self.app.sceneWidgetData())

    def sizeHint(self):
        return QSize(600, 540)


class TDataTableGrid(QTableView):
    def __init__(self, app, parent=None):
        self.app: object = app
        super(TDataTableGrid, self).__init__(parent)
        model = GraModel(self.app.t_dataWidgetData, self.app.t_dataDimension)
        self.setModel(model)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.verticalHeader().setDefaultSectionSize(self.rowHeight(0))
        self.app.modelChanged.connect(self.update)

    def update(self):
        self.model().layoutChanged.emit()


class TPathTableGrid(QTableView):
    def __init__(self, app, parent=None):
        self.app:object = app
        super(TPathTableGrid, self).__init__(parent)
        model = GraModel(self.app.t_pathWidgetData, self.app.t_pathDimension)
        self.setModel(model)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.verticalHeader().setDefaultSectionSize(self.rowHeight(0))
        self.app.modelChanged.connect(self.update)

    def update(self):
        self.model().layoutChanged.emit()
