# coding=utf-8
import unittest
from dbms import DBMS


class DBMS_Test01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dbms = DBMS()

    def test_01addNode_Root(self):
        tOutput = [{'node': 1, 'parent': 1}]
        self.assertEqual(self.dbms.lastLabel, 0)
        self.dbms.addNode()
        res = self.dbms.listDataTable()
        self.assertEqual(self.dbms.lastLabel, 1)
        self.assertEqual(res, tOutput)

    def test_02addNode_Many(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 2, 'parent': 1},
                        {'node': 3, 'parent': 2},
                        {'node': 4, 'parent': 2},
                        {'node': 5, 'parent': 2},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 6},
                        {'node': 8, 'parent': 6}]
        t_pathOutput = [(2, 1),
                        (3, 2),
                        (3, 1),
                        (4, 2),
                        (4, 1),
                        (5, 2),
                        (5, 1),
                        (6, 1),
                        (7, 6),
                        (7, 1),
                        (8, 6),
                        (8, 1)]
        self.assertEqual(self.dbms.lastLabel, 1)
        self.dbms.addNode(1)
        self.dbms.addNode(2)
        self.dbms.addNode(2)
        self.dbms.addNode(2)
        self.dbms.addNode(1)
        self.dbms.addNode(6)
        self.dbms.addNode(6)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 8)

    def test_03addNode9(self):
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
                        (3, 2),
                        (3, 1),
                        (4, 2),
                        (4, 1),
                        (5, 2),
                        (5, 1),
                        (6, 1),
                        (7, 6),
                        (7, 1),
                        (8, 6),
                        (8, 1),
                        (9, 2),
                        (9, 1)]
        self.assertEqual(self.dbms.lastLabel, 8)
        self.dbms.addNode(2)
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
        self.dbms.addNode()
        self.dbms.addNode(1)
        self.dbms.addNode(2)
        self.dbms.addNode(2)
        self.dbms.addNode(2)
        self.dbms.addNode(1)
        self.dbms.addNode(6)
        self.dbms.addNode(6)
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
                        (3, 2),
                        (3, 1),
                        (5, 2),
                        (5, 1),
                        (6, 1),
                        (7, 6),
                        (7, 1),
                        (8, 6),
                        (8, 1)]
        self.dbms.deleteNode(4)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 8)

        del t_dataOutput[-1]
        del t_pathOutput[-1]
        del t_pathOutput[-1]
        self.dbms.deleteNode(8)
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
        self.dbms.addNode()
        self.dbms.addNode(1)
        self.dbms.addNode(2)
        self.dbms.addNode(2)
        self.dbms.addNode(2)
        self.dbms.addNode(1)
        self.dbms.addNode(6)
        self.dbms.addNode(6)
        self.dbms.addNode(6)
        self.assertEqual(self.dbms.lastLabel, 9)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        # pprint(t_dataRes)
        # pprint(t_pathRes)

    def test_02moveSubtree_2_7(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 2, 'parent': 7},
                        {'node': 3, 'parent': 2},
                        {'node': 4, 'parent': 2},
                        {'node': 5, 'parent': 2},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 6},
                        {'node': 8, 'parent': 6},
                        {'node': 9, 'parent': 6}]
        t_pathOutput = [(3, 2),
                        (4, 2),
                        (5, 2),
                        (6, 1),
                        (7, 6),
                        (7, 1),
                        (8, 6),
                        (8, 1),
                        (9, 6),
                        (9, 1),
                        (2, 7),
                        (2, 6),
                        (2, 1),
                        (3, 7),
                        (4, 7),
                        (5, 7),
                        (3, 6),
                        (3, 1),
                        (4, 6),
                        (4, 1),
                        (5, 6),
                        (5, 1)
                        ]
        # t_pathRes = self.dbms.listPathTable()
        # pprint(t_pathRes)

        self.dbms.moveSubtree1(2, 7)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()

        # pprint(t_dataRes)
        # pprint(t_pathRes)
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 9)


class DBMS_Test04(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dbms = DBMS()

    def test_01createTree(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 2, 'parent': 1},
                        {'node': 3, 'parent': 2},
                        {'node': 4, 'parent': 2},
                        {'node': 5, 'parent': 2},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 6},
                        {'node': 8, 'parent': 6}]
        t_pathOutput = [(2, 1),
                        (3, 2),
                        (3, 1),
                        (4, 2),
                        (4, 1),
                        (5, 2),
                        (5, 1),
                        (6, 1),
                        (7, 6),
                        (7, 1),
                        (8, 6),
                        (8, 1)]
        self.dbms.addNode()
        self.dbms.addNode(1)
        self.dbms.addNode(2)
        self.dbms.addNode(2)
        self.dbms.addNode(2)
        self.dbms.addNode(1)
        self.dbms.addNode(6)
        self.dbms.addNode(6)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 8)

    def test_02_1_addLeafNode9(self):
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
                        (3, 2),
                        (3, 1),
                        (4, 2),
                        (4, 1),
                        (5, 2),
                        (5, 1),
                        (6, 1),
                        (7, 6),
                        (7, 1),
                        (8, 6),
                        (8, 1),
                        (9, 2),
                        (9, 1)]
        self.dbms.addNode(2)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 9)

    def test_03_2_deleteNode4(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 2, 'parent': 1},
                        {'node': 3, 'parent': 2},
                        {'node': 5, 'parent': 2},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 6},
                        {'node': 8, 'parent': 6},
                        {'node': 9, 'parent': 2}]
        t_pathOutput = [(2, 1),
                        (3, 2),
                        (3, 1),
                        (5, 2),
                        (5, 1),
                        (6, 1),
                        (7, 6),
                        (7, 1),
                        (8, 6),
                        (8, 1),
                        (9, 2),
                        (9, 1)]
        self.dbms.deleteNode(4)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 9)

    def test_04_3_MoveLeafNode3(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 2, 'parent': 1},
                        {'node': 3, 'parent': 6},
                        {'node': 5, 'parent': 2},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 6},
                        {'node': 8, 'parent': 6},
                        {'node': 9, 'parent': 2}]
        t_pathOutput = [(2, 1),
                        (5, 2),
                        (5, 1),
                        (6, 1),
                        (7, 6),
                        (7, 1),
                        (8, 6),
                        (8, 1),
                        (9, 2),
                        (9, 1),
                        (3, 6),
                        (3, 1)]
        self.dbms.moveNode(3, 6)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 9)

    def test_05_6_MoveSubtree_2_7(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 2, 'parent': 7},
                        {'node': 3, 'parent': 6},
                        {'node': 5, 'parent': 2},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 6},
                        {'node': 8, 'parent': 6},
                        {'node': 9, 'parent': 2}]
        t_pathOutput = [(5, 2),
                        (6, 1),
                        (7, 6),
                        (7, 1),
                        (8, 6),
                        (8, 1),
                        (9, 2),
                        (3, 6),
                        (3, 1),
                        (2, 7),
                        (2, 6),
                        (2, 1),
                        (5, 7),
                        (9, 7),
                        (5, 6),
                        (5, 1),
                        (9, 6),
                        (9, 1)]
        # t_pathRes = self.dbms.listPathTable()
        # pprint(t_pathRes)
        self.dbms.moveSubtree1(2, 7)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        # pprint(t_pathRes)
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 9)

    def test_06_4_InsertNode_10(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 2, 'parent': 7},
                        {'node': 3, 'parent': 6},
                        {'node': 5, 'parent': 2},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 10},
                        {'node': 8, 'parent': 6},
                        {'node': 9, 'parent': 2},
                        {'node': 10, 'parent': 6}]
        t_pathOutput = [(5, 2),
                        (6, 1),
                        (8, 6),
                        (8, 1),
                        (9, 2),
                        (3, 6),
                        (3, 1),
                        (2, 7),
                        (5, 7),
                        (9, 7),
                        (10, 6),
                        (10, 1),
                        (7, 10),
                        (7, 6),
                        (7, 1),
                        (2, 10),
                        (5, 10),
                        (9, 10),
                        (2, 6),
                        (2, 1),
                        (5, 6),
                        (5, 1),
                        (9, 6),
                        (9, 1)]
        self.dbms.insertNode(7)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 10)

    def test_07_5_RemoveNode_2(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 3, 'parent': 6},
                        {'node': 5, 'parent': 7},
                        {'node': 6, 'parent': 1},
                        {'node': 7, 'parent': 10},
                        {'node': 8, 'parent': 6},
                        {'node': 9, 'parent': 7},
                        {'node': 10, 'parent': 6}]
        t_pathOutput = [(6, 1),
                        (8, 6),
                        (8, 1),
                        (3, 6),
                        (3, 1),
                        (5, 7),
                        (9, 7),
                        (10, 6),
                        (10, 1),
                        (7, 10),
                        (7, 6),
                        (7, 1),
                        (5, 10),
                        (9, 10),
                        (5, 6),
                        (5, 1),
                        (9, 6),
                        (9, 1)]
        self.dbms.removeNode(2)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 10)

    def test_08_7_DeleteSubtree_7(self):
        t_dataOutput = [{'node': 1, 'parent': 1},
                        {'node': 3, 'parent': 6},
                        {'node': 6, 'parent': 1},
                        {'node': 8, 'parent': 6},
                        {'node': 10, 'parent': 6}]
        t_pathOutput = [(6, 1),
                        (8, 6),
                        (8, 1),
                        (3, 6),
                        (3, 1),
                        (10, 6),
                        (10, 1)]
        self.dbms.deleteSubtree(7)
        t_dataRes = self.dbms.listDataTable()
        t_pathRes = self.dbms.listPathTable()
        # pprint(t_pathRes)
        self.assertEqual(t_dataRes, t_dataOutput)
        self.assertEqual(t_pathRes, t_pathOutput)
        self.assertEqual(self.dbms.lastLabel, 10)

if __name__ == '__main__':
    unittest.main()
