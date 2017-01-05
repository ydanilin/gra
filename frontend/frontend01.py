# coding=utf-8


class FrontEnd:
    def __init__(self, dbms, gviz):
        self.dbms = dbms
        self.gviz = gviz
        self.graph = []
        self.boundingBox = {}
        self.columns = 2
        self.nodesCount = 0
        self.redrawState = True

    def setRedrawState(self, state):
        self.redrawState = state

    def setGraphName(self, name):
        self.gviz.name = name

    def setDirected(self, directed):
        self.gviz.directed = directed

    def setNodesDefaultShape(self, shape):
        self.gviz.nodesDefaultShape = shape

    def loadGraph(self):
        # DB operations
        self.graph = self.dbms.listDataTable()
        self.nodesCount = len(self.graph)
        # Gviz operations
        self.gviz.newGraph(self.graph)
        self.boundingBox = self.gviz.makeLayout()
        self.gviz.getGeometry(self.graph)

    def addChildNode(self, parent):
        # DB operations
        self.dbms.addChildNode(parent)
        self.graph = self.dbms.listDataTable()
        self.nodesCount = len(self.graph)
        # Gviz operations
        if self.redrawState:
            self.gviz.newGraph(self.graph)
            self.boundingBox = self.gviz.makeLayout()
            self.gviz.getGeometry(self.graph)
        else:
            print('not implemented')

    # datafeeds for widgets
    def t_dataData(self, row, column):
        # TODO seems should be datagrid based on list of dictionaries...
        col = 'node'
        if column == 0:
            col = 'node'
        if column == 1:
            col = 'parent'
        return self.graph[row][col]

    def t_dataDimension(self, whichDimension):
        output = None
        if whichDimension == 1:
            output = self.nodesCount
        if whichDimension == 2:
            output = self.columns
        return output
