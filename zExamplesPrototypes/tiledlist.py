# coding=utf-8
import sys
from PyQt5.QtWidgets import QApplication
from tiledlist import TiledListView


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = TiledListView()
    view.show()
    sys.exit(app.exec_())
