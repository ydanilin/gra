# coding=utf-8
import os
import sys
from PyQt5.QtWidgets import QApplication, QTreeView
from dbms import DBMS
from epygraph import Epygraph
from frontend import FrontEnd
from models import TreeModel


if __name__ == '__main__':
    ownPath = os.path.dirname(os.path.abspath(__file__))
    dbPath = os.path.join(ownPath, 'dbms', 'ierarch01.db')
    dbms = DBMS(dbPath)
    ep = Epygraph()
    frontEnd = FrontEnd(dbms, ep)
    frontEnd.loadGraph(True)

    model = TreeModel(frontEnd.graphData['nodes'])
    model.preorder()

    app = QApplication(sys.argv)
    view = QTreeView()
    view.setModel(model)
    view.setWindowTitle("Simple Tree Model")
    view.show()
    sys.exit(app.exec_())
