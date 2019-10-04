# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 11:38:05 2019

@author: ElJocho
"""
import unittest
import field as fld
import objects
import controller as ctr


class test_field(unittest.TestCase):
    """used for testing field module"""
    def test_init(self):
        """test if field is succesfully initiated"""
        f = fld.field()
        assert f.size == len(f.grid) ** 2
        assert f.grid[49, 49] == 0
        assert f.grid[49, 43] == 0
        with self.assertRaises(IndexError):
            f.grid[50, 49]

    def test_checkCell(self):
        """check if Check Cell returns correct values"""
        f = fld.field()
        assert f.checkCell([49, 49]) == 0
        assert f.checkCell([3, 49]) == 0
        with self.assertRaises(IndexError):
            f.checkCell([50, 1])

    def test_setCell(self):
        """check if setCell handles values correctly"""
        f = fld.field()
        assert f.checkCell([49, 2]) == 0
        f.setCell([49, 2], 1)
        assert f.checkCell([49, 2]) == 1
        with self.assertRaises(ValueError):
            f.setCell([2, 6], 3)
        with self.assertRaises(IndexError):
            f.setCell([69, 6], 1)


class test_ant(unittest.TestCase):
    """used for testing ant module"""
    def test_init(self):
        """test if ant is correctly initialized"""
        a = objects.ant()
        assert a.alive is True
        assert a.age == 0
        assert a.location is None

    def test_die(self):
        """check if ants die if told so"""
        a = objects.ant()
        assert a.alive is True
        a.die()
        assert a.alive is False

    def test_getOlder(self):
        """check if ants age the right way and die if they age 81 times"""
        a = objects.ant()
        assert a.age == 0
        for age in range(1, 80):
            a.getOlder()
            assert a.age == age
            assert a.alive is True
        a.getOlder()
        assert a.alive is False

    def test_move(self):
        """test if ants move in the right direction and age afterwards"""
        a = objects.ant()
        a.move()
        assert a.age == 1

    def test_ant_names(self):
        """test if ant names are requested correctly"""
        names = objects.get_ant_names()
        assert type(names) is list
        assert len(names) == 40


class test_food(unittest.TestCase):
    def test_food(self):
        food = objects.food()
        food.amount = 20
        food.location = [1, 2]
        food.changeAmount(3)
        assert food.amount == 23
        food.changeAmount(-4)
        assert food.amount == 19
        assert food.getX() == food.location[0]


class test_controller(unittest.TestCase):
    pass


if "__main__" == __name__:
    unittest.main()
