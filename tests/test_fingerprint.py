# -*- coding: utf-8 -*-

import sys
sys.path.append('src/')

import unittest
from fingerprint import fingerprint


class TestFinterprint(unittest.TestCase):


    def test_sql_simple(self):
        self.assertEqual(fingerprint('SELECT * FROM tbl WHERE col1 = "abc"'),
                         "select * from tbl where col1 = ?")

    def test_sql_simple2(self):
        self.assertEqual(fingerprint('SELECT * FROM tbl WHERE col1 = 123'),
                         "select * from tbl where col1 = ?")

    def test_sql_wherein(self):
        self.assertEqual(fingerprint('SELECT * FROM tbl WHERE id IN ("a", "b", 123)'),
                         "select * from tbl where id in(?+)")

    def test_sql_japanese(self):
        self.assertEqual(fingerprint('SELECT * FROM tbl WHERE col1 LIKE "%ソ%"'),
                         "select * from tbl where col1 like ?")

    def test_sql_multiline(self):
        self.assertEqual(fingerprint("SELECT col1, created_at FROM tbl\nWHERE col1 like 'abc%'"),
                         "select col1, created_at from tbl where col1 like ?")

    def test_sql_limit(self):
        self.assertEqual(fingerprint('SELECT * FROM tbl WHERE col1 = "abc" LIMIT 10'),
                         "select * from tbl where col1 = ? limit ?")

    def test_sql_call(self):
        self.assertEqual(fingerprint("CALL MYFUNCTION(123)"),
                         "call myfunction(?)")

    def test_sql_long(self):
        self.assertEqual(fingerprint("SELECT *, sleep(1) from tbl where pk = 1 or pk = 2 or pk = 3 or pk = 4 or pk = 5 or pk = 6 or pk = 7 or pk = 8 or pk = 9 or pk = 10 or pk = 11"),
                         "select *, sleep(?) from tbl where pk = ? or pk = ? or pk = ? or pk = ? or pk = ? or pk = ? or pk = ? or pk = ? or pk = ? or pk = ? or pk = ?")
