# coding=utf-8
import epygraph.gvzpassage as gps


class Epygraph:
    def __init__(self):
        self.name = 'Untitled'
        self.directed = True
        self.nodesDefaultShape = 'circle'
        self.graphPtr = None
        self.nodePtrs = {}

    def newGraph(self, nodes):
        if self.graphPtr:
            gps.agraphClose(self.graphPtr)
        self.nodePtrs = {}
        self.graphPtr = gps.agraphNew(self.name, self.directed)
        gps.set_shape_nodes(self.graphPtr, self.nodesDefaultShape)
        for node in nodes:
            label = node['node']
            parent = node['parent']
            self.nodePtrs[label] = self.addNode(label, parent)

    def addNode(self, label, parent):
        nodePtr = gps.addNode(self.graphPtr, str(label))
        # since each node has one and only one edge TO PARENT,
        # each node record of nodePtrs dict (keys = labels) represents a pair
        # (nodePtr, edgePtr), where edgePtr points to edge to parent
        # if it is a root node, edgePtr will be None
        if parent != label:
            parentPtr = self.nodePtrs[parent][0]
            edgePtr = gps.addEdge(self.graphPtr, parentPtr, nodePtr)
        else:
            edgePtr = None
        return nodePtr, edgePtr

    def makeLayout(self):
        return gps.layout(self.graphPtr)

    def getGeometry(self, nodes):
        for node in nodes:
            label = node['node']
            if label in self.nodePtrs:
                nodePtr = self.nodePtrs[label][0]
                edgePtr = self.nodePtrs[label][1]
                node['geometry'] = gps.node_geometry(nodePtr)
                if edgePtr:
                    node['edgeGeometry'] = gps.edge_geometry(edgePtr)
                else:
                    node['edgeGeometry'] = None
        gps.clearContext(self.graphPtr)


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
