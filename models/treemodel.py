# coding=utf-8
from PyQt5.QtCore import (Qt, QSize,
                          QAbstractItemModel, QIdentityProxyModel,
                          QModelIndex)
from .treeitem import TreeItem


class TreeModel(QAbstractItemModel):
    def __init__(self, datta, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem: object = None
        self.columns: dict = {0: ['node'],
                              1: ['parent'],
                              2: ['geometry', 'centerX'],
                              3: ['userData']}
        self.columnsAmt = len(self.columns)
        # rootData = []
        # rootData.append('Label')
        # rootData.append('Summary')
        # self.rootItem = TreeItem(rootData)
        self.setupModelData(datta)

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

    def columnCount(self, parent=None):
        # if parent.isValid():
        #     return parent.internalPointer().columnCount()
        # else:
        #     return self.rootItem.columnCount()
        return self.columnsAmt

    def data(self, index, role=None):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.datta(self.columns[index.column()])

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return super(TreeModel, self).flags(index)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section][-1]
        return None

    def setupModelData(self, graData):
        appearedNodes = {}
        for item in graData:
            node = item['node']
            parent = item['parent']
            # columnData = [str(node)]
            columnData = item
            if node != parent:
                parentNode = appearedNodes[parent]
                # record node itself
                appearedNodes[node] = TreeItem(columnData, parentNode)
                # and add it to it's parent children
                parentNode.appendChild(appearedNodes[node])
            else:
                appearedNodes[node] = TreeItem(columnData, None)
                self.rootItem = appearedNodes[node]

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


class TreeViewModel(QIdentityProxyModel):
    def __init__(self, sourceModel, parent=None):
        super(TreeViewModel, self).__init__(parent)
        self.setSourceModel(sourceModel)
        self.nameMapping = {'node': 'Label',
                            'parent': 'Parent label',
                            'centerX': 'Center X',
                            'userData': 'Description'}

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and (role == Qt.DisplayRole or
                                             role == Qt.SizeHintRole):
            modelHeader = self.sourceModel().columns[section][-1]
            mappedName = modelHeader
            if modelHeader in self.nameMapping.keys():
                mappedName = self.nameMapping[modelHeader]
            if role == Qt.DisplayRole:
                return mappedName
            # if role == Qt.SizeHintRole:
            #     return QSize(300, 30)
        return None

    def data(self, index, role=None):
        # "||" = logical OR in C++
        if role == Qt.DisplayRole or role == Qt.EditRole:
            output = self.sourceModel().data(index, role)
            if index.column() in [2]:
                output = str(round(output, 1))
            return output
        if role == Qt.TextAlignmentRole:
            if index.column() in [1, 2]:
                return Qt.AlignCenter
        else:
            return None

    def setData(self, index, value, role=None):
        if index.isValid() and role == Qt.EditRole:
            puk = 1

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        output = super(TreeViewModel, self).flags(index)
        if index.column() == 3:
            output = output | Qt.ItemIsEditable  # "|" = bitwise OR Python
        return output                            # "|" = bitwise OR C++

# http://stackoverflow.com/questions/32822442/how-to-align-text-of-table-widget-in-qt
