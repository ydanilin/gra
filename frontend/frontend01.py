# coding=utf-8


class FrontEnd:
    def __init__(self, dbms, gviz):
        self.dbms: object = dbms
        self.gviz: object = gviz
        self.graphData: dict = {}
        self.columns: int = 2
        self.nodesCount: int = 0
        self.redrawState: bool = True
        self.tPath: list = []
        self.tPathCount = 0

    def setRedrawState(self, state):
        self.redrawState = state

    def setGraphName(self, name):
        self.gviz.name = name

    def setDirected(self, directed):
        self.gviz.directed = directed

    def setNodesDefaultShape(self, shape):
        self.gviz.nodesDefaultShape = shape

    def loadGraph(self, forceRedraw):
        # DB operations
        self.graphData = self.dbms.listDataTable()
        self.nodesCount = len(self.graphData)
        self.tPath = self.dbms.listPathTable()
        self.tPathCount = len(self.tPath)
        # Gviz operations
        if forceRedraw:
            self.gviz.newGraph(self.graphData)
            self.graphData[0]['boundingBox'] = self.gviz.makeLayout()
            self.gviz.getGeometry(self.graphData)
        else:
            print('not implemented')

    def addChildNode(self, parent: int):
        # DB operations
        self.dbms.addNode(parent)
        self.loadGraph(self.redrawState)

    def deleteLeafNode(self, node: int):
        # DB operations
        atWhichParent = self.dbms.deleteLeafNode(node)  # ret val needed if no
        self.loadGraph(self.redrawState)

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
        return self.graphData[row][col]

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
