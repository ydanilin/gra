# coding=utf-8
import unittest
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
                        UniqueConstraint, select)
from dbms.dbms01 import DBMS


class DBMS_Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dbms = DBMS()
        # cls.data_ins = cls.dbms.t_data.insert(prefixes=['OR IGNORE'])
        # cls.data_list = [
        #     {'node': 1, 'parent': 1}
            # {'node': 2, 'parent': 1},
            # {'node': 3, 'parent': 2},
            # {'node': 4, 'parent': 2},
            # {'node': 5, 'parent': 2},
            # {'node': 6, 'parent': 1},
            # {'node': 7, 'parent': 6},
            # {'node': 8, 'parent': 6}
        # ]
        # cls.path_ins = cls.dbms.t_path.insert().prefix_with('OR IGNORE')
        # cls.path_list = [
        #     {'node': 2, 'ancestor': 1},
        #     {'node': 3, 'ancestor': 1},
        #     {'node': 3, 'ancestor': 2},
        #     {'node': 4, 'ancestor': 1},
        #     {'node': 4, 'ancestor': 2},
        #     {'node': 5, 'ancestor': 1},
        #     {'node': 5, 'ancestor': 2},
        #     {'node': 6, 'ancestor': 1},
        #     {'node': 7, 'ancestor': 1},
        #     {'node': 7, 'ancestor': 6},
        #     {'node': 8, 'ancestor': 1},
        #     {'node': 8, 'ancestor': 6}
        # ]
        # cls.dbms.connection.execute(cls.data_ins, cls.data_list)
        # cls.dbms.connection.execute(cls.path_ins, cls.path_list)

    def test_addChildNode_Root(self):
        tOutput = [{'node': 1, 'parent': 1}]
        self.dbms.addChildNode(None)
        res = self.dbms.listDataTable()
        self.assertEqual(self.dbms.lastLabel, 1)
        self.assertEqual(res, tOutput)

    def test_addNode_Many(self):
        tOutput = [{'node': 1, 'parent': 1}]

if __name__ == '__main__':
    unittest.main()
