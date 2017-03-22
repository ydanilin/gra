# coding=utf-8
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtCore import QAbstractItemModel, QModelIndex
from .treeitem import TreeItem


class TreeModel(QAbstractItemModel):
    def __init__(self, datta, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem: object = None
        rootData = []
        rootData.append('Label')
        # rootData.append('Summary')
        self.rootItem = TreeItem(rootData)
        self.setupModelData(datta, self.rootItem)

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parentItem: object = None
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem or parentItem == None:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.datta(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return super(TreeModel, self).flags(index)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.datta(section)
        return None

    def setupModelData(self, graList, rootParent):
        appearedNodes = {}
        for item in graList:
            node = item['node']
            parent = item['parent']
            if node != parent:
                columnData = [str(node)]
                appearedNodes[node] = TreeItem(columnData, appearedNodes[parent])
                appearedNodes[parent].appendChild(appearedNodes[node])
            else:
                appearedNodes[node] = rootParent

    def preorder(self):
        cNodeIndex = self.createIndex(0, 0, self.rootItem)
        stack: list = []
        while True:
            if cNodeIndex.isValid():
                print(self.data(cNodeIndex, Qt.DisplayRole))
                stack.append(cNodeIndex)
                cNodeIndex = self.index(0, 0, cNodeIndex)
            else:
                if not stack:
                    return
                cNodeIndex = stack.pop()
                row = cNodeIndex.row()
                column = cNodeIndex.column()
                cNodeIndex = cNodeIndex.sibling(row + 1, column)
