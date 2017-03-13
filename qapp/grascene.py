# coding=utf-8
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem
from PyQt5.QtCore import QCoreApplication
from qapp.nodeshape import NodeShape


class GraScene(QGraphicsScene):
    def __init__(self):
        super(GraScene, self).__init__()

    def drawScene(self, graphData:list):
        nodes = graphData[0]
        boundingBox = graphData[1]
        self.clear()
        scaleDpi = 101.0 / 72.0  # (true res for 344x193 mm, 1366x768) / 72
        LLx = boundingBox['LLx']
        LLy = boundingBox['LLx']
        URx = boundingBox['URx']
        URy = boundingBox['URy']
        self.addRect(LLx * scaleDpi, LLy * scaleDpi,
                      URx * scaleDpi, URy * scaleDpi)
        scale = 96  # maybe this is because GV uses 96 dpi and operates in inches
        for node in nodes:
            ng = node['geometry']
            x = ng['centerX'] * scaleDpi
            y = (URy - ng['centerY']) * scaleDpi
            rx = (ng['width'] / 2) * scale
            ry = (ng['height'] / 2) * scale
            label = node['node']
            el = NodeShape(x - rx, y - ry, 2 * rx, 2 * ry, label)
            lbl = QGraphicsTextItem(self.tr(str(label)), el)
            # TODO: text positioniong
            lbl.setAcceptHoverEvents(False)
            # TODO: try to make child.event()
            lbl.setPos(x, y)
            self.addItem(el)
            # node's edge to parent
            eg = node['edgeGeometry']
            if eg:
                # TODO: edges hover
                spl = eg[0]
                if not spl['sflag']:
                    start = spl['points'][0]
                else:
                    start = spl['sarrowtip']
                if not spl['eflag']:
                    end = spl['points'][-1]
                else:
                    end = spl['earrowtip']
                x1 = start['x'] * scaleDpi
                y1 = (URy - start['y']) * scaleDpi
                x2 = end['x'] * scaleDpi
                y2 = (URy - end['y']) * scaleDpi
                self.addLine(x1, y1, x2, y2)
