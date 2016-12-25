# coding=utf-8
import sys
from qapp import QApp
from dbms import DBMS
from epygraph import Epygraph


if __name__ == '__main__':
    app = QApp(sys.argv)
    ep = Epygraph(app.mainwindow.sc)
    dbms = DBMS(ep)
    app.dbms = dbms
    app.drawGraph('DjHuj')
    app.mainwindow.show()
    sys.exit(app.exec_())
