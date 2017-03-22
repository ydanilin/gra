# coding=utf-8


class TreeItem:
    def __init__(self, datta, parentItem=None):
        self.parentItem: object = parentItem
        self.childItems: list = []
        self.itemData: list = datta

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def row(self):
        output = 0
        if self.parentItem:
            output = self.parentItem.childItems.index(self)
        return output

    def columnCount(self):
        return len(self.itemData)

    def datta(self, column):
        output = None
        if column < self.columnCount():
            output = str(self.itemData[column])
        return output

    def parent(self):
        return self.parentItem
