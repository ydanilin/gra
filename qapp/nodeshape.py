# coding=utf-8
from PyQt5.QtWidgets import QGraphicsEllipseItem, QMenu
from PyQt5.QtGui import QPen, QColor


class NodeShape(QGraphicsEllipseItem):
    def __init__(self, x, y, width, height, label):
        super(NodeShape, self).__init__(x, y, width, height)
        self.label:int = label
        self.oldpen:object = None
        self.oldTextColor:object = None
        self.setAcceptHoverEvents(True)

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
        callerWidget = event.widget()
        menu = QMenu('Node', callerWidget)
        addNode = menu.addAction(callerWidget.tr('Add child node here'))
        addNode.triggered.connect(self.addChildNode)
        if not callerWidget.parent().app.hasChildren(self.label):
            delLeaf = menu.addAction(callerWidget.tr('Delete leaf node'))
            delLeaf.triggered.connect(self.deleteLeafNode)
        menu.popup(event.screenPos())

    # handlers
    def addChildNode(self):
        app = self.scene().views()[0].app
        app.addChildNodeEvent(self.label)
        self.scene().drawScene(app.sceneWidgetData())

    def deleteLeafNode(self):
        app = self.scene().views()[0].app
        app.deleteLeafNodeEvent(self.label)
        self.scene().drawScene(app.sceneWidgetData())
