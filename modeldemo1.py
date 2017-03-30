# coding=utf-8
import os
import sys
from PyQt5.QtWidgets import QApplication, QTreeView
from dbms import DBMS
from epygraph import Epygraph
from frontend import FrontEnd
from models import TreeModel, TreeViewModel, ExpModel


if __name__ == '__main__':
    ownPath = os.path.dirname(os.path.abspath(__file__))
    dbPath = os.path.join(ownPath, 'dbms', 'ierarch01.db')
    dbms = DBMS(dbPath)
    ep = Epygraph()
    frontEnd = FrontEnd(dbms, ep)
    frontEnd.loadGraph(True)

    model = TreeModel(frontEnd.graphData)
    # model.preorder()
    # model_1 = TreeViewModel(model)
    model_1 = ExpModel(model)

    app = QApplication(sys.argv)
    view = QTreeView()
    view.setModel(model_1)
    # view.header().setMinimumSectionSize(1)
    view.setWindowTitle("Simple Tree Model")
    view.show()
    view.expandAll()
    sys.exit(app.exec_())
