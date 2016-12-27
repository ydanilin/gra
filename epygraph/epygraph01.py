# coding=utf-8
import epygraph.gvzpassage as gps


class Epygraph:
    def __init__(self, graScene=None):
        self.graScene = graScene
        self.graphPtr = None
        self.nodePtrs = {}
        self.edgePtrs = {}
        self.boundingBox = None

    def loadGraph(self, nodes, name='Untitled', directed=True):
        if self.graphPtr:
            gps.agraphClose(self.graphPtr)
        self.nodePtrs = {}
        self.edgePtrs = {}
        self.graphPtr = gps.agraphNew(name, directed)
        gps.set_shape_nodes(self.graphPtr, 'circle')
        for node in nodes:
            label = node[0]
            parent = node[1]
            # create node
            self.nodePtrs[label] = gps.addNode(self.graphPtr, str(label))
            # create edge
            if parent != label:
                key = '{0}-{1}'.format(parent, label)
                self.edgePtrs[key] = gps.addEdge(self.graphPtr,
                                                 self.nodePtrs[parent],
                                                 self.nodePtrs[label])
            # else:
            #     print('This is root node')
        self.boundingBox = gps.layout(self.graphPtr)
        # transfer pointer to self
        if self.graScene:
            self.graScene.drawScene(self)
            return 0
        else:
            return -1

    def addNode(self, label, parent):
        self.nodePtrs[label] = gps.addNode(self.graphPtr, str(label))
        # create edge
        if parent != label:
            key = '{0}-{1}'.format(parent, label)
            self.edgePtrs[key] = gps.addEdge(self.graphPtr,
                                             self.nodePtrs[parent],
                                             self.nodePtrs[label])
        # else:
        #     print('This is root node')
        self.boundingBox = gps.layout(self.graphPtr)
        # transfer pointer to self
        if self.graScene:
            self.graScene.drawScene(self)
            return 0
        else:
            return -1

    def deleteNode(self, label, parent):
        node = self.nodePtrs.pop(label)
        edge = self.edgePtrs.pop('{0}-{1}'.format(parent, label))
        gps.delete_edge(self.graphPtr, edge)
        gps.delete_node(self.graphPtr, node)
        self.boundingBox = gps.layout(self.graphPtr)
        if self.graScene:
            self.graScene.drawScene(self)
            return 0
        else:
            return -1

    def nodeGeometry(self, nodePtr):
        return gps.node_geometry(nodePtr)

    def edgeGeometry(self, edgePtr):
        return gps.edge_geometry(edgePtr)
