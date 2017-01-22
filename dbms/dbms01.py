# coding=utf-8
from pprint import pprint
from sqlalchemy.sql import text
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
                        UniqueConstraint, select, update, and_, or_, column,
                        literal_column, union)


# inspector = inspect(engine)
# inspector.get_columns('book')
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
                            Column('id_', Integer(), primary_key=True),
                            Column('node', Integer()),
                            Column('ancestor', Integer()),
                            UniqueConstraint('node', 'ancestor',
                                             name='path_entry')
                            )
        self.metadata.create_all(self.engine)
        self.lastLabel = 0

    def listDataTable(self):
        nodes = []
        res = self.connection.execute(select([self.t_data.c.node,
                                              self.t_data.c.parent]
                                             ).order_by(self.t_data.c.node)
                                      )
        nodes = [{'node': l[0], 'parent': l[1]} for l in res]
        # self.lastLabel = nodes[-1]['node']
        return nodes

    def listPathTable(self):
        res = self.connection.execute(select([self.t_path.c.node,
                                              self.t_path.c.ancestor]).order_by
                                                            (self.t_path.c.id_)
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
            subset = select([column('node'), column('ancestor')]).select_from\
                (
                union(select([literal_column('1').label('sortir'),
                              literal_column(str(self.lastLabel)).label('node'),
                              literal_column(str(parent)).label('ancestor')]),
                      select([2, self.lastLabel, self.t_path.c.ancestor]).where
                          (self.t_path.c.node == parentLabel)
                      ).order_by('sortir')
                 )
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
        if label == self.lastLabel:
            self.lastLabel -= 1
        return parent

    def moveSubtree(self, label, moveTo):
        # update t_data
        upd = update(self.t_data).where(self.t_data.c.node == label).values(
            parent=moveTo)
        self.connection.execute(upd)

        # update t_path
        subtree = select([self.t_path.c.node]).where(self.t_path.c.ancestor == label)
        path = select([self.t_path.c.ancestor]).where(self.t_path.c.node == label)

        # deletion
        cond = and_(or_(self.t_path.c.node == label,
                        self.t_path.c.node.in_(subtree)),
                    self.t_path.c.ancestor.in_(path)
                    )
        delet = self.t_path.delete().where(cond)
        self.connection.execute(delet)

        # insertion
        subtree = select([self.t_path.c.node]).where(self.t_path.c.ancestor == label)
        path = select([self.t_path.c.ancestor]).where(self.t_path.c.node == label)
        path_y = select([self.t_path.c.ancestor]).where\
            (self.t_path.c.node == moveTo).order_by(self.t_path.c.id_.asc())

        res = self.connection.execute(text("""
        SELECT * FROM t_path"""))
        lst = [l for l in res]
        pprint(lst)
        print(moveTo)
        res = self.connection.execute(text("""
            SELECT * FROM t_path WHERE node = 7"""))
        lst = [l for l in res]
        pprint(lst)
        print(str(path_y))
        res = self.connection.execute(path_y)
        lst = [l for l in res]
        pprint(lst)


        subset = select([column('node'), column('ancestor')]).select_from\
            (
            union(select([literal_column('1').label('sortir'),
                          literal_column(str(label)).label('node'),
                          literal_column(str(moveTo)).label('ancestor')]
                         ),
                  select([2, label, path_y]),
                  select([3, subtree, moveTo]),
                  select([4, subtree, path_y])
                  ).order_by('sortir')
            )
        addToPath = self.t_path.insert().from_select(
            ['node', 'ancestor'], subset)
        print(str(addToPath))
        self.connection.execute(addToPath)

    def moveSubtree1(self, label, moveTo):
        # update t_data
        upd = update(self.t_data).where(self.t_data.c.node == label).values(
            parent=moveTo)
        self.connection.execute(upd)

        # update t_path
        subtree = select([self.t_path.c.node]).where(
            self.t_path.c.ancestor == label)
        path = select([self.t_path.c.ancestor]).where(
            self.t_path.c.node == label)

        # deletion
        cond = and_(or_(self.t_path.c.node == label,
                        self.t_path.c.node.in_(subtree)),
                    self.t_path.c.ancestor.in_(path)
                    )
        delet = self.t_path.delete().where(cond)
        self.connection.execute(delet)

        # insertion
        subtree = select([self.t_path.c.node]).where(
            self.t_path.c.ancestor == label)
        path = select([self.t_path.c.ancestor]).where(
            self.t_path.c.node == label)
        path_y = select([self.t_path.c.ancestor]).where \
            (self.t_path.c.node == moveTo).order_by(self.t_path.c.id_.asc())
        addToPath = text("""
            INSERT INTO t_path (node, ancestor)
            SELECT node, ancestor FROM (
            SELECT 1 AS sortir, :label AS node, :moveTo AS ancestor, 0 as ku
            UNION
            SELECT 2, :label, ancestor, id_ FROM t_path
                                             WHERE node = :moveTo
            UNION
            SELECT 3, node, :moveTo, id_ FROM t_path
                                          WHERE ancestor = :label
            UNION
            SELECT 4, a.node, b.ancestor, 0 as ku FROM t_path a, (SELECT node, ancestor FROM t_path WHERE node = :moveTo order by id_) b
                                           WHERE a.ancestor = :label
            ORDER BY sortir, ku)""")
        self.connection.execute(addToPath, {'label': label, 'moveTo': moveTo})

