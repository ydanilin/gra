# coding=utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractTableModel


class GraModel(QAbstractTableModel):
    def __init__(self, dataProc, dimProc):
        super(GraModel, self).__init__()
        self.dataProc = dataProc
        self.dimProc = dimProc

    def rowCount(self, parent):
        return self.dimProc(1)

    def columnCount(self, parent):
        return self.dimProc(2)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.dataProc(index.row(), index.column())
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return ' node '
                if section == 1:
                    return 'parent'
        return super(GraModel, self).headerData(section, orientation, role)
