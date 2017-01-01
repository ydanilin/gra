# coding=utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractTableModel


class GraModel(QAbstractTableModel):
    def __init__(self, tableDataProc):
        super(GraModel, self).__init__()
        self.table = tableDataProc()
        self.rows = len(self.table)
        self.columns = len(self.table[0])

    def rowCount(self, parent):
        return self.rows

    def columnCount(self, parent):
        return self.columns

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.table[index.row()][index.column()]
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
