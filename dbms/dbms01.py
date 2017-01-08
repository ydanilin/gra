# coding=utf-8
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
                        UniqueConstraint, select)


class DBMS:
    def __init__(self, database=None):
        if database:
            address = 'sqlite:///' + database
        else:
            address = 'sqlite://'
        self.engine = create_engine(address)
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

    def listPathTable(self):
        res = self.connection.execute(select([self.t_path.c.node,
                                              self.t_path.c.ancestor])
                                      )
        path = [l for l in res]
        return path

    def addChildNode(self, parent, child=None):
        """supply parent = None to add root label"""
        self.lastLabel += 1
        if parent:
            parentLabel = parent
        else:
            parentLabel = self.lastLabel  # this means we're adding root node
        addToData = self.t_data.insert().values((self.lastLabel, parentLabel))
        self.connection.execute(addToData)
        if parent:
            subset = select([self.lastLabel, parentLabel]).union(
                select([self.lastLabel, self.t_path.c.ancestor]).where(
                    self.t_path.c.node == parentLabel))
            addToPath = self.t_path.insert().from_select(
                ['node', 'ancestor'], subset)
            self.connection.execute(addToPath)

    def deleteLeafNode(self, label):
        parent = self.connection.execute(
            select([self.t_data.c.parent]).where(self.t_data.c.node == label)
        ).first()[0]
        delFromData = self.t_data.delete().where(self.t_data.c.node == label)
        delFromPath = self.t_path.delete().where(self.t_path.c.node == label)
        self.connection.execute(delFromData)
        self.connection.execute(delFromPath)
        return parent
