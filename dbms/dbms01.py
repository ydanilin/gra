# coding=utf-8
import os
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
                        UniqueConstraint, select)


class DBMS:
    def __init__(self):
        ownPath = os.path.dirname(os.path.abspath(__file__))
        dbPath = os.path.join(ownPath, 'ierarch01.db')
        self.engine = create_engine('sqlite:///' + dbPath)
        self.connection = self.engine.connect()
        self.metadata = MetaData()

        self.t_data = Table('t_data', self.metadata,
                            Column('node', Integer(), primary_key=True),
                            Column('parent', Integer(), nullable=False)
                            )
        self.t_path = Table('t_path', self.metadata,
                            Column('node', Integer()),
                            Column('ancestor', Integer()),
                            UniqueConstraint('node', 'ancestor',
                                             name='path_entry')
                            )
        self.metadata.create_all(self.engine)
        self.lastLabel = 0

    def listDataTable(self):
        res = self.connection.execute(select([self.t_data.c.node,
                                              self.t_data.c.parent]
                                             ).order_by(self.t_data.c.node)
                                      )
        nodes = [{'node': l[0], 'parent': l[1]} for l in res]
        self.lastLabel = nodes[-1]['node']
        return nodes

    def addChildNode(self, parentLabel, child=None, forceReGraph=False):
        self.lastLabel += 1
        addToData = self.t_data.insert().values((self.lastLabel, parentLabel))
        subset = select([self.lastLabel, parentLabel]).union(
            select([self.lastLabel, self.t_path.c.ancestor]).where(
                self.t_path.c.node == parentLabel))
        addToPath = self.t_path.insert().from_select(
            ['node', 'ancestor'], subset)
        self.connection.execute(addToData)
        self.connection.execute(addToPath)
        # if forceReGraph=False then call addNode
        # else call loadGraph
        if not forceReGraph:
            self.gviz.addNode(self.lastLabel, parentLabel)
        else:
            nodes = self.listDataTable()
            self.gviz.loadGraph(nodes, 'redrawn')
        return 0

    def deleteLeafNode(self, label, forceReGraph=False):
        parent = self.connection.execute(
            select([self.t_data.c.parent]).where(self.t_data.c.node == label)
        ).first()[0]
        delFromData = self.t_data.delete().where(self.t_data.c.node == label)
        delFromPath = self.t_path.delete().where(self.t_path.c.node == label)
        self.connection.execute(delFromData)
        self.connection.execute(delFromPath)
        if not forceReGraph:
            self.gviz.deleteNode(label, parent)
        else:
            nodes = self.listDataTable()
            self.gviz.loadGraph(nodes, 'redrawn')
        return 0
