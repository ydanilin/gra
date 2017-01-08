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
        self.tPath = []
        self.tPathCount = 0

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
        self.tPath = self.dbms.listPathTable()
        self.tPathCount = len(self.tPath)
        # Gviz operations
        self.gviz.newGraph(self.graph)
        self.boundingBox = self.gviz.makeLayout()
        self.gviz.getGeometry(self.graph)

    def addChildNode(self, parent):
        # DB operations
        self.dbms.addChildNode(parent)
        self.graph = self.dbms.listDataTable()
        self.nodesCount = len(self.graph)
        self.tPath = self.dbms.listPathTable()
        self.tPathCount = len(self.tPath)
        # Gviz operations
        if self.redrawState:
            self.gviz.newGraph(self.graph)
            self.boundingBox = self.gviz.makeLayout()
            self.gviz.getGeometry(self.graph)
        else:
            print('not implemented')

    def deleteLeafNode(self, node):
        # DB operations
        atWhichParent = self.dbms.deleteLeafNode(node)  # ret val needed if no
        self.graph = self.dbms.listDataTable()          # redraw
        self.nodesCount = len(self.graph)
        self.tPath = self.dbms.listPathTable()
        self.tPathCount = len(self.tPath)
        # Gviz operations
        if self.redrawState:
            self.gviz.newGraph(self.graph)
            self.boundingBox = self.gviz.makeLayout()
            self.gviz.getGeometry(self.graph)
        else:
            print('not implemented')

    # service functions for context menu events
    def hasChildren(self, label):
        found = False
        for record in self.tPath:
            if record[1] == label:
                found = True
                break
        return found

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

    def t_pathData(self, row, column):
        return self.tPath[row][column]

    def t_pathDimension(self, whichDimension):
        output = None
        if whichDimension == 1:
            output = self.tPathCount
        if whichDimension == 2:
            output = self.columns
        return output
