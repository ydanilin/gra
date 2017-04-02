# coding=utf-8
from PyQt5.QtCore import (Qt, QSize,
                          QAbstractItemModel, QIdentityProxyModel,
                          QModelIndex, QAbstractProxyModel)
from .treeitem import TreeItem


class TreeModel(QAbstractItemModel):
    def __init__(self, datta, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem: object = None
        self.columns: dict = {0: ['node'],
                              1: ['parent'],
                              2: ['geometry'],
                              3: ['edgeGeometry'],
                              4: ['userData'],
                              5: ['geometry', 'centerX'],
                              6: ['geometry', 'centerY']}
        self.columnsAmt = len(self.columns)
        self.setupModelData(datta)
        # model, proc, row, col, assData, role
        self.msg = 'S\t{0}\t{1}\t{2}\t{3}\t{4}'
        self.roles = {0: 'DisplayRole',
                      1: 'DecorationRole',
                      2: 'EditRole',
                      3: 'ToolTipRole',
                      4: 'StatusTipRole',
                      5: 'WhatsThisRole',
                      6: 'FontRole',
                      7: 'TextAlignmentRole',
                      8: 'BackgroundRole',
                      9: 'ForegroundRole',
                      10: 'CheckStateRole',
                      11: 'AccessibleTextRole',
                      12: 'AccessibleDescriptionRole',
                      13: 'SizeHintRole',
                      14: 'InitialSortOrderRole'
                      }

    def index(self, row, column, parent=None, *args, **kwargs):
        # DEBUG
        assData = None
        if parent.isValid():
            assData = parent.internalPointer().datta(['node'])
        print(self.msg.format('index()', row, column, assData, 'N/A'))
        # DEBUG ends
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
        # DEBUG
        row = index.row()
        column = index.column()
        assData = None
        if index.isValid():
            assData = index.internalPointer().datta(['node'])
        print(self.msg.format('parent()', row, column, assData, 'N/A'))
        # DEBUG ends
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem or parentItem == None:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=None, *args, **kwargs):
        # DEBUG
        row = parent.row()
        column = parent.column()
        assData = None
        if parent.isValid():
            assData = parent.internalPointer().datta(['node'])
        print(self.msg.format('rowCount()', row, column, assData, 'N/A'))
        # DEBUG ends
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def columnCount(self, parent=None, *args, **kwargs):
        # DEBUG
        row = parent.row()
        column = parent.column()
        assData = None
        if parent.isValid():
            assData = parent.internalPointer().datta(['node'])
        print(self.msg.format('columnCount()', row, column, assData, 'N/A'))
        # DEBUG ends
        # if parent.isValid():
        #     return parent.internalPointer().columnCount()
        # else:
        #     return self.rootItem.columnCount()
        return self.columnsAmt

    def data(self, index, role=None):
        # DEBUG
        row = index.row()
        column = index.column()
        assData = None
        if index.isValid():
            assData = index.internalPointer().datta(['node'])
        roll = 'Not Listed'
        if role in self.roles.keys():
            roll = self.roles[role]
        print(self.msg.format('data()', row, column, assData, roll))
        # DEBUG ends
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return str(item.datta(self.columns[index.column()]))

    def flags(self, index):
        # DEBUG
        row = index.row()
        column = index.column()
        assData = None
        if index.isValid():
            assData = index.internalPointer().datta(['node'])
        print(self.msg.format('flags()', row, column, assData, 'N/A'))
        # DEBUG ends
        if not index.isValid():
            return Qt.NoItemFlags
        return super(TreeModel, self).flags(index)

    def headerData(self, section, orientation, role=None):
        # DEBUG
        row = 'ori:' + str(orientation)
        column = section
        assData = None
        roll = 'Not Listed'
        if role in self.roles.keys():
            roll = self.roles[role]
        print(self.msg.format('headerData()', row, column, assData, roll))
        # DEBUG ends
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section][-1]
        return None

    def setupModelData(self, graData):
        appearedNodes = {}
        for item in graData:
            node = item['node']
            parent = item['parent']
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
        return output  # "|" = bitwise OR C++


# http://stackoverflow.com/questions/32822442/how-to-align-text-of-table-widget-in-qt


class ExpModel(QAbstractProxyModel):
    def __init__(self, sourceModel, parent=None):
        super(ExpModel, self).__init__(parent)
        self.setSourceModel(sourceModel)
        self.sourceIndexes: list = [6, 0, 5]
        self.columnsAmt: int = len(self.sourceIndexes)

    def mapFromSource(self, sourceIndex):
        sCol = sourceIndex.column()
        print(sCol)
        if sCol in self.sourceIndexes:
            return self.createIndex(sourceIndex.row(),
                                    self.sourceIndexes.index(sCol),
                                    sourceIndex.internalPointer())
        # if sCol == -1:
        #     return self.createIndex(sourceIndex.row(), sCol,
        #                             sourceIndex.internalPointer())
        else:
            return self.createIndex(sourceIndex.row(), sCol,
                                    sourceIndex.internalPointer())

    def mapToSource(self, index):
        requestedColumn = index.column()
        # print(requestedColumn)
        if requestedColumn == -1:
            return self.sourceModel().createIndex(index.row(),
                                                  requestedColumn,
                                                  index.internalPointer())
        mappedColumn = self.sourceIndexes[requestedColumn]
        return self.sourceModel().createIndex(index.row(),
                                              mappedColumn,
                                              index.internalPointer())

    def rowCount(self, parent=None, *args, **kwargs):
        return self.sourceModel().rowCount(parent)

    def columnCount(self, parent=None, *args, **kwargs):
        return self.columnsAmt

    def index(self, row, column, parent=None, *args, **kwargs):
        sourceParent = self.mapToSource(parent)
        sourceIndex = self.sourceModel().index(row, column, sourceParent)
        return self.mapFromSource(sourceIndex)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return 'Puk'
        return None

    def parent(self, index=None):
        sourceIndex = self.mapToSource(index)
        sourceParent = sourceIndex.parent()
        return self.mapFromSource(sourceParent)

        # def flags(self, index):
        #     if not index.isValid():
        #         return Qt.NoItemFlags
        #     return super(ExpModel, self).flags(index)

# http://stackoverflow.com/questions/23896182/sourcemodel-createindex-in-qabstractproxymodel-sub-class?rq=1
