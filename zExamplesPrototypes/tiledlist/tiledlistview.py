# coding=utf-8
from PyQt5.QtCore import Qt, QCoreApplication, QRectF
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QAbstractItemView


class TiledListView(QAbstractItemView):
    def __init__(self, parent=None):
        super(TiledListView, self).__init__(parent)
        self.idealWidth: int = 0
        self.idealHeight: int = 0
        self.rectForRow: dict = {}
        self.hashIsDirty: bool = False
        self.setFocusPolicy(Qt.WheelFocus)
        fnt = QCoreApplication.instance().font('QListView')
        self.setFont(fnt)
        self.horizontalScrollBar().setRange(0, 0)
        self.verticalScrollBar().setRange(0, 0)
        self.extraHeight = 3

    def setModel(self, model):
        super(TiledListView, self).setModel(model)
        self.hashIsDirty = True

    def calculateRectsIfNecessary(self):
        if not self.hashIsDirty:
            return
        extraWidth = 10
        fm = QFontMetrics(self.font())
        rowHeight = fm.height() + self.extraHeight
        maxWidth = self.viewport().width()
        minimumWidth = 0
        x = 0
        y = 0
        for row in range(self.model().rowCount(self.rootIndex())):
            index = self.model().index(row, 0, self.rootIndex())
            text = str(self.model().data(index))
            textWidth = fm.width(text)
            # "||" = logical OR C++
            # "&&" = logical AND C++
            if not(x == 0 or (x + textWidth + extraWidth < maxWidth)):
                y += rowHeight
                x = 0
            if x != 0:
                x += extraWidth
            self.rectForRow[row] = QRectF(x, y, textWidth + extraWidth,
                                          rowHeight)
            if textWidth > minimumWidth:
                minimumWidth = textWidth
                x += textWidth
        self.idealWidth = minimumWidth + extraWidth
        self.idealHeight = y + rowHeight
        self.hashIsDirty = False
        self.viewport().update()

