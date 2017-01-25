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

        # add to t_data
        if parent:
            parentLabel = parent
        else:
            parentLabel = self.lastLabel  # this means we're adding root node
        addToData = self.t_data.insert().values((self.lastLabel, parentLabel))
        self.connection.execute(addToData)

        # add to t_path
        if parent:
            sort_val1 = literal_column('1').label('sort_group')
            sort_val2 = literal_column('2').label('sort_group')
            x = literal_column(str(self.lastLabel)).label('node')
            y = literal_column(str(parent)).label('ancestor')
            path_parent = select([self.t_path.c.ancestor]).where\
                                 (self.t_path.c.node == parentLabel)
            subset = select([column('node'), column('ancestor')]).select_from\
                (
                union(select([sort_val1, x, y]),
                      select([sort_val2, x, path_parent])
                      ).order_by('sort_group')
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
            (self.t_path.c.node == moveTo)

        subset = select([column('node'), column('ancestor')]).select_from\
            (
            union(select([literal_column('1').label('sort_group'),
                          literal_column(str(label)).label('node'),
                          literal_column(str(moveTo)).label('ancestor')]
                         ),
                  select([2, label, path_y]),
                  select([3, subtree, moveTo]),
                  select([4, subtree, path_y])
                  ).order_by('sort_group')
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
            SELECT 1 AS sort_group, :label AS node, :moveTo AS ancestor, 0 as sort_node, 0 as sort_anc
            UNION
            SELECT 2, :label, ancestor, 0, id_ FROM t_path
                                             WHERE node = :moveTo
            UNION
            SELECT 3, node, :moveTo, id_, 0 FROM t_path
                                          WHERE ancestor = :label
            UNION
            SELECT 4, a.node, b.ancestor, a.id_, b.id_ FROM t_path a, t_path b
                                           WHERE a.ancestor = :label AND b.node = :moveTo
            ORDER BY sort_group, sort_node, sort_anc)""")
        self.connection.execute(addToPath, {'label': label, 'moveTo': moveTo})

# TODO: try to implement math names (x, y)
# TODO: sorting in add_node
# TODO: rewrite insertion based on this
