# coding=utf-8
import sys
from qapp import QApp
from dbms import DBMS
from epygraph import Epygraph
from frontend import FrontEnd


if __name__ == '__main__':
    dbms = DBMS()
    ep = Epygraph()
    frontend = FrontEnd(dbms, ep)
    app = QApp(sys.argv, frontend)
    app.mainwindow.show()
    sys.exit(app.exec_())
