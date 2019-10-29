# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 11:38:05 2019

@author: ElJocho
"""
import unittest
import src.field as fld
import src.objects as objects


class TestField(unittest.TestCase):
    """used for testing Field module"""
    def test_init(self):
        """test if Field is succesfully initiated"""
        f = fld.Field()
        assert f.grid[49, 49] == 0
        assert f.grid[49, 43] == 0
        with self.assertRaises(IndexError):
            f.grid[50, 49]

    def test_checkCell(self):
        """check if Check Cell returns correct values"""
        f = fld.Field()
        assert f.check_cell([49, 49]) == 0
        assert f.check_cell([3, 49]) == 0
        with self.assertRaises(IndexError):
            f.check_cell([50, 1])

    def test_setCell(self):
        """check if set_cell handles values correctly"""
        f = fld.Field()
        assert f.check_cell([49, 2]) == 0
        f.set_cell([49, 2], 1)
        assert f.check_cell([49, 2]) == 1
        with self.assertRaises(IndexError):
            f.set_cell([69, 6], 1)


class TestAnt(unittest.TestCase):
    """used for testing Ant module"""
    def test_init(self):
        """test if Ant is correctly initialized"""
        a = objects.Ant()
        assert a.alive is True
        assert a.age == 0
        assert a.location is None

    a = objects.Ant()
    a.location =[10, 10]
    f = fld.Field()

    def test_die(self):
        """check if ants die if told so"""
        assert self.a.alive is True
        self.a.die()
        assert self.a.alive is False
        self.a.alive = True

    def test_getOlder(self):
        """check if ants age the right way and die if they age 101 times"""
        assert self.a.age == 0
        for age in range(1, 101):
            self.a.get_older(self.f)
            assert self.a.age == age
            assert self.a.alive is True
        self.a.get_older(self.f)
        assert self.a.alive is False
        self.a.alive = True
        self.a.age = 0

    def test_move(self):
        """test if ants move in the right direction and age afterwards"""
        foods = [objects.Food([0, 0])]
        a2 = objects.Ant()
        a2.location = [0, 0]
        hive = objects.Hive([12, 10])
        ants = [self.a, a2]
        self.a.move(ants, foods, hive, self.f)
        assert self.a.age == 1
        assert self.a.next == [9, 9]
        self.a.has_food = True
        self.a.move(ants, foods, hive, self.f)
        assert self.a.age == 2
        assert self.a.next == [11, 10]

    def test_ant_names(self):
        """test if Ant names are requested correctly"""
        pass
        assert len(self.a.names) == 0
        names = self.a.get_ant_names()
        assert type(self.a.names) is list
        assert len(self.a.names) == 40
        assert self.a.name is None
        self.a.set_name()
        assert self.a.name is not None


class TestFood(unittest.TestCase):
    def test_food(self):
        food = objects.Food()
        food.amount = 20
        food.location = [1, 2]
        food.nom()
        assert food.amount == 19
        assert food.get_x() == food.location[0]


class TestUtils(unittest.TestCase):
    pass

class TestController(unittest.TestCase):
    pass


if "__main__" == __name__:
    unittest.main()
