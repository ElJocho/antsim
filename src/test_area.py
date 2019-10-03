# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 11:38:05 2019

@author: ElJocho
"""
import unittest
import field as fld
import ant


class test_field(unittest.TestCase):
    def test_init(self):
        f = fld.field()
        assert f.size == len(f.grid) ** 2
        assert f.grid[49, 49] == 2
        assert f.grid[49, 43] == 0
        with self.assertRaises(IndexError):
            f.grid[50, 49]

    def test_checkCell(self):
        f = fld.field()
        assert f.checkCell([49, 49]) == 2
        assert f.checkCell([3, 49]) == 0

    def test_setCell(self):
        f = fld.field()
        assert f.checkCell([49, 2]) == 0
        f.setCell([49, 2], 1)
        assert f.checkCell([49, 2]) == 1
        with self.assertRaises(ValueError):
            f.setCell([2, 6], 3)
        with self.assertRaises(ValueError):
            f.setCell([69, 6], 1)


class test_ant(unittest.TestCase):
    def test_init(self):
        a = ant.ant()
        assert a.alive is True
        assert a.age == 0
        assert a.location is None

    def test_die(self):
        a = ant.ant()
        assert a.alive is True
        a.die()
        assert a.alive is False

    def test_getOlder(self):
        a = ant.ant()
        assert a.age == 0
        for age in range(1, 80):
            a.getOlder()
            assert a.age == age
            assert a.alive is True
        a.getOlder()
        assert a.alive is False

    def test_move(self):
        a = ant.ant()
        a.move()
        assert a.age == 1

    def test_ant_names(self):
        names = ant.get_ant_names()
        assert type(names) is list
        assert len(names) == 40


if "__main__" == __name__:
    unittest.main()
