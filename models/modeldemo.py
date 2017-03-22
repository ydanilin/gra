# coding=utf-8
import sys
from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtWidgets import QApplication, QTreeView
from treemodel import TreeModel


if __name__ == '__main__':

    app = QApplication(sys.argv)

    f = QFile('default.txt')
    f.open(QIODevice.ReadOnly)
    output = f.readAll()

    model = TreeModel(str(output))
    f.close()

    view = QTreeView()
    view.setModel(model)
    view.setWindowTitle("Simple Tree Model")
    view.show()
    sys.exit(app.exec_())
