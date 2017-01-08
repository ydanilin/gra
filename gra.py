# coding=utf-8
import os
import sys
from qapp import QApp
from dbms import DBMS
from epygraph import Epygraph
from frontend import FrontEnd


if __name__ == '__main__':
    ownPath = os.path.dirname(os.path.abspath(__file__))
    dbPath = os.path.join(ownPath, 'dbms', 'ierarch01.db')
    dbms = DBMS(dbPath)
    ep = Epygraph()
    frontend = FrontEnd(dbms, ep)
    app = QApp(sys.argv, frontend)
    app.mainwindow.show()
    sys.exit(app.exec_())
