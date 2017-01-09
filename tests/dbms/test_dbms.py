# coding=utf-8
import unittest
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
                        UniqueConstraint, select)
from dbms.dbms01 import DBMS
from pprint import pprint


class DBMS_Test01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dbms = DBMS()

    def test_01addChildNode_Root(self):
        tOutput = [{'node': 1, 'parent': 1}]
        self.assertEqual(self.dbms.lastLabel, 0)
        self.dbms.addChildNode(None)
        res = self.dbms.listDataTable()
        self.assertEqual(self.dbms.lastLabel, 1)
        self.assertEqual(res, tOutput)

    def test_02addChildNode_Many(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 2, 'parent': 1},
                        {'node': 3, 'parent': 2},
                        {'node': 4, 'parent': 2},
                        {'node': 5, 'parent': 2},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 6},
                        {'node': 8, 'parent': 6}]
        t_pathOutput = [(2, 1),
                        (3, 1),
                        (3, 2),
                        (4, 1),
                        (4, 2),
                        (5, 1),
                        (5, 2),
                        (6, 1),
                        (7, 1),
                        (7, 6),
                        (8, 1),
                        (8, 6)]
        self.assertEqual(self.dbms.lastLabel, 1)
        self.dbms.addChildNode(1)
        self.dbms.addChildNode(2)
        self.dbms.addChildNode(2)
        self.dbms.addChildNode(2)
        self.dbms.addChildNode(1)
        self.dbms.addChildNode(6)
        self.dbms.addChildNode(6)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 8)

    def test_03addChildNode9(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 2, 'parent': 1},
                        {'node': 3, 'parent': 2},
                        {'node': 4, 'parent': 2},
                        {'node': 5, 'parent': 2},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 6},
                        {'node': 8, 'parent': 6},
                        {'node': 9, 'parent': 2}]
        t_pathOutput = [(2, 1),
                        (3, 1),
                        (3, 2),
                        (4, 1),
                        (4, 2),
                        (5, 1),
                        (5, 2),
                        (6, 1),
                        (7, 1),
                        (7, 6),
                        (8, 1),
                        (8, 6),
                        (9, 1),
                        (9, 2)]
        self.assertEqual(self.dbms.lastLabel, 8)
        self.dbms.addChildNode(2)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 9)


class DBMS_Test02(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dbms = DBMS()

    def test_01addNodes(self):
        self.dbms.addChildNode(None)
        self.dbms.addChildNode(1)
        self.dbms.addChildNode(2)
        self.dbms.addChildNode(2)
        self.dbms.addChildNode(2)
        self.dbms.addChildNode(1)
        self.dbms.addChildNode(6)
        self.dbms.addChildNode(6)
        self.assertEqual(self.dbms.lastLabel, 8)

    def test_02deleteNode4(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 2, 'parent': 1},
                        {'node': 3, 'parent': 2},
                        {'node': 5, 'parent': 2},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 6},
                        {'node': 8, 'parent': 6}]
        t_pathOutput = [(2, 1),
                        (3, 1),
                        (3, 2),
                        (5, 1),
                        (5, 2),
                        (6, 1),
                        (7, 1),
                        (7, 6),
                        (8, 1),
                        (8, 6)]
        self.dbms.deleteLeafNode(4)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 8)

        del t_dataOutput[-1]
        del t_pathOutput[-1]
        del t_pathOutput[-1]
        self.dbms.deleteLeafNode(8)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 7)


class DBMS_Test03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dbms = DBMS()

    def test_01addNodes(self):
        self.dbms.addChildNode(None)
        self.dbms.addChildNode(1)
        self.dbms.addChildNode(2)
        self.dbms.addChildNode(2)
        self.dbms.addChildNode(2)
        self.dbms.addChildNode(1)
        self.dbms.addChildNode(6)
        self.dbms.addChildNode(6)
        self.dbms.addChildNode(6)
        self.assertEqual(self.dbms.lastLabel, 9)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        # pprint(t_dataRes)
        # pprint(t_pathRes)

    def test_02moveSubtree_2_7(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 6},
                        {'node': 2, 'parent': 7},
                        {'node': 3, 'parent': 2},
                        {'node': 4, 'parent': 2},
                        {'node': 5, 'parent': 2},
                        {'node': 8, 'parent': 6},
                        {'node': 9, 'parent': 6}]
        t_pathOutput = [(6, 1),
                        (7, 6),
                        (7, 1),
                        (2, 7),
                        (2, 6),
                        (2, 1),
                        (3, 2),
                        (3, 7),
                        (3, 6),
                        (3, 1),
                        (4, 2),
                        (4, 7),
                        (4, 6),
                        (4, 1),
                        (5, 2),
                        (5, 7),
                        (5, 6),
                        (5, 1),
                        (8, 6),
                        (8, 1),
                        (9, 6),
                        (9, 1)
                        ]
        self.dbms.moveSubtree(2, 7)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()

        pprint(t_dataRes)
        pprint(t_pathRes)
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 9)


if __name__ == '__main__':
    unittest.main()
