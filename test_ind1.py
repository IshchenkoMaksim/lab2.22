#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Для индивидуального задания лабораторной работы 2.21 добавьте тесты с
использованием модуля unittest, проверяющие операции по работе с базой данных.
"""

import sqlite3
import ind1
import unittest
from pathlib import Path
import tempfile
import shutil


class IndTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path_dir = Path(self.tmp.name)
        shutil.copyfile(ind1.load(), self.path_dir / 'test.db')
        self.fullpath = self.path_dir / 'test.db'
        self.conn = sqlite3.connect(self.fullpath)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            SELECT way.number, routes.destination, way.time
            FROM way
            INNER JOIN routes ON routes.route_id = way.route_id
            WHERE routes.route_id == 1
            """
        )
        rows = self.cursor.fetchall()
        self.result = [
            {
                "number": row[0],
                "destination": row[1],
                "time": row[2],
            }
            for row in rows
        ]

    def test_create_db(self):
        self.cursor.execute(
            """
            SELECT name FROM sqlite_master WHERE type = 'table'
            AND name = 'routes' OR name = 'way'
            """
        )
        table = self.cursor.fetchall()
        self.assertEqual(table, [('routes',), ('way',)])

    def test_add_route(self):
        ind1.add_route(self.fullpath, 1, 'text', 'text')
        self.cursor.execute(
            """
            SELECT way.number, routes.destination, way.time
            FROM way
            INNER JOIN routes ON routes.route_id = way.route_id
            WHERE way.route_id = (SELECT MAX(route_id) FROM way)
            """
        )
        rows = self.cursor.fetchall()
        self.last = [
            {
                "number": row[0],
                "destination": row[1],
                "time": row[2],
            }
            for row in rows
        ]
        self.assertEqual(
            self.last,
            [{'number': 1,
              'destination': 'text',
              'time': 'text'}]
        )

    def test1_select_route_1(self):
        self.assertListEqual(
            self.result,
            [{'number': 2,
              'destination': 'Moscow',
              'time': '10:00'}]
        )

    def test1_select_route_2(self):
        self.assertNotEqual(
            self.result,
            [{'number': 3,
              'destination': 'Kiev',
              'time': '14:30'}]
        )

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()


if __name__ == '__main__':
    unittest.main()
