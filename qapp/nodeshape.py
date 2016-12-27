# coding=utf-8
from PyQt5.QtWidgets import QGraphicsEllipseItem, QMenu
from PyQt5.QtGui import QPen, QColor


class NodeShape(QGraphicsEllipseItem):
    def __init__(self, x, y, width, height, label):
        super(NodeShape, self).__init__(x, y, width, height)
        self.label = label
        self.setAcceptHoverEvents(True)
        self.oldpen = None
        self.oldTextColor = None

    def hoverEnterEvent(self, event):
        color = QColor('red')
        self.oldpen = self.pen()
        self.setPen(QPen(color))
        for child in self.childItems():
            # I know this is shitty solution, we will crash if children are
            # not of text type...
            self.oldTextColor = child.defaultTextColor()
            child.setDefaultTextColor(color)

    def hoverLeaveEvent(self, event):
        if self.oldpen:
            self.setPen(self.oldpen)
        if self.oldTextColor:
            for child in self.childItems():
                child.setDefaultTextColor(self.oldTextColor)

    def contextMenuEvent(self, event):
        # http://www.qtcentre.org/threads/5187-Popup-menu-for-a-QGraphicsItem
        # if use asynchronous call, ALWAYS pass a parent - event.widget()
        # to menu constructor, otherwise the menu will be destroyed immediately
        # as having zero reference
        menu = QMenu('Node', event.widget())
        addNode = menu.addAction(event.widget().tr('Add child node here'))
        delLeaf = menu.addAction(event.widget().tr('Delete leaf node'))
        menu.popup(event.screenPos())
        addNode.triggered.connect(self.addChildNode)
        delLeaf.triggered.connect(self.deleteLeafNode)

    # handlers
    def addChildNode(self):
        self.scene().app.addChildNode(self.label)

    def deleteLeafNode(self):
        self.scene().app.deleteLeafNode(self.label)
