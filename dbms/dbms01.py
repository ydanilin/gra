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
        self.lastLabel: int = 0
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
                            Column('ancestor', Integer())#,
                            # UniqueConstraint('node', 'ancestor',
                            #                  name='path_entry')
                            )
        self.metadata.create_all(self.engine)
        nodes = self.listDataTable()
        if nodes:
            self.lastLabel = nodes[-1]['node']

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

    # **********************************
    # Public interface functions
    def addNode(self, attachTo: int = 0):
        """supply parent = None to add root label"""
        # internal names
        # x - new node label; y - parent to attach to
        self.lastLabel += 1
        x = self.lastLabel
        # add to t_data
        if attachTo:
            y = attachTo
        else:
            y = x  # this means we're adding root node
        self.addLeafNode(x, y)
        return x

    def deleteNode(self, node:int):
        self.deleteLeafNode(node)

    def moveNode(self, node:int, moveTo:int):
        self.deleteLeafNode(node)
        self.addLeafNode(node, moveTo)

    def insertNode(self, insertBefore:int):
        y = self.retrieveParent(insertBefore)
        self.lastLabel += 1
        x = self.lastLabel
        self.addLeafNode(x, y)
        self.moveSubtree1(insertBefore, x)
        return x

    def removeNode(self, node:int):
        y = self.retrieveParent(node)
        self.deleteLeafNode(node)
        self.branchUpSubtree(node, y)

    def deleteSubtree(self, atNode:int):
        self.deleteLeafNode(atNode)
        self.wipeOffSubtree(atNode)

    # ***********************************
    # Internal functions
    def addLeafNode(self, x: int, y: int):
        addToData = self.t_data.insert().values((x, y))
        self.connection.execute(addToData)
        # add to t_path
        if y != x:
            gr1 = literal_column('1').label('sort_group')
            gr2 = literal_column('2').label('sort_group')
            vs0 = literal_column('0').label('sort_value')

            X = literal_column(str(x)).label('node')
            Y = literal_column(str(y)).label('ancestor')

            path_parent = select([self.t_path.c.ancestor,
                                  self.t_path.c.id_]).where\
                                 (self.t_path.c.node == y)

            subset = select([column('node'), column('ancestor')]).select_from\
                (
                union(select([gr1, X, Y, vs0]),
                      select([gr2, X, path_parent])
                      ).order_by('sort_group', 'sort_value')
                 )
            addToPath = self.t_path.insert().from_select(
                ['node', 'ancestor'], subset)
            self.connection.execute(addToPath)

    def deleteLeafNode(self, x:int):
        if x == self.lastLabel:
            self.lastLabel -= 1
        delFromData = self.t_data.delete().where(self.t_data.c.node == x)
        delFromPath = self.t_path.delete().where(
            self.t_path.c.node == x)
        self.connection.execute(delFromData)
        self.connection.execute(delFromPath)

    def branchUpSubtree(self, x:int, y:int):
        """x = nodeToDelete, y = newParent"""
        updData = update(self.t_data).where(
            self.t_data.c.parent == x).values(parent=y)
        delFromPath = self.t_path.delete().where(self.t_path.c.ancestor == x)
        self.connection.execute(updData)
        self.connection.execute(delFromPath)

    def wipeOffSubtree(self, x:int):
        node = self.t_path.c.node
        ancestor = self.t_path.c.ancestor
        subtree = select([node]).where(ancestor == x)
        delFromPath = self.t_path.delete().where(node.in_(subtree))
        delFromData = self.t_data.delete().where(self.t_data.c.parent == x)
        self.connection.execute(delFromPath)
        self.connection.execute(delFromData)

    def moveSubtree(self, label:int, moveTo:int):
        x = label
        y = moveTo
        # update t_data
        upd = update(self.t_data).where(self.t_data.c.node == x).values(
            parent=y)
        self.connection.execute(upd)

        node = self.t_path.c.node
        ancestor = self.t_path.c.ancestor
        id_ = self.t_path.c.id_

        # update t_path
        subtree = select([node]).where(ancestor == x)
        path = select([ancestor]).where(node == x)

        # deletion
        cond = and_(or_(node == x,
                        node.in_(subtree)),
                    ancestor.in_(path)
                    )
        delet = self.t_path.delete().where(cond)
        self.connection.execute(delet)

        # insertion
        subtree = select([node, id_]).where(ancestor == x)
        path_y = select([ancestor, id_]).where(node == y)

        gs1 = literal_column('1').label('sort_group')
        gs2 = literal_column('2').label('sort_group')
        gs3 = literal_column('3').label('sort_group')
        gs4 = literal_column('4').label('sort_group')
        sn0 = literal_column('0').label('sort_node')
        sa0 = literal_column('0').label('sort_ancestor')
        X = literal_column(str(x)).label('node')
        Y = literal_column(str(y)).label('ancestor')
        subset = select([column('node'), column('ancestor')]).select_from\
            (
            union(select([gs1, X, sn0, Y, sa0]),
                  select([gs2, X, sn0, path_y]),
                  select([gs3, subtree, Y, sa0]),
                  select([gs4, subtree, path_y])
                  ).order_by('sort_group', 'sort_node', 'sort_ancestor')
            )
        addToPath = self.t_path.insert().from_select(
            ['node', 'ancestor'], subset)
        print(str(addToPath))
        self.connection.execute(addToPath)

    def moveSubtree1(self, label:int, moveTo:int):
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
        # x = label
        # node = self.t_path.c.node
        # ancestor = self.t_path.c.ancestor
        # clause1 = and_(or_(node == x, node.in_(subtree)),
        #                ancestor.in_(path)
        #                )
        #
        # clause2 = and_(node.in_(subtree), ancestor == x)
        # cond = or_(clause1, clause2)
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

    def retrieveParent(self, node:int):
        parent = self.connection.execute(
            select([self.t_data.c.parent]).where(self.t_data.c.node == node)
        ).first()[0]
        return parent
