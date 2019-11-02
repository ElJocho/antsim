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
    field = fld.Field()

    def test_init(self):
        """test if Field is succesfully initiated"""
        init_test_field = fld.Field()
        assert init_test_field.grid[49, 49] == 0
        assert init_test_field.grid[49, 43] == 0
        with self.assertRaises(IndexError):
            init_test_field.grid[50, 49]

    def test_check_cell(self):
        """check if Check Cell returns correct values"""
        assert self.field.check_cell([49, 49]) == 0
        assert self.field.check_cell([3, 49]) == 0
        with self.assertRaises(IndexError):
            self.field.check_cell([50, 1])

    def test_set_cell(self):
        """check if set_cell handles values correctly"""
        assert self.field.check_cell([49, 2]) == 0
        self.field.set_cell([49, 2], 1)
        assert self.field.check_cell([49, 2]) == 1
        with self.assertRaises(IndexError):
            self.field.set_cell([69, 6], 1)


class TestAnt(unittest.TestCase):
    """used for testing Ant module"""

    ant = objects.Ant()
    field = fld.Field()
    ant.location = [10, 10]

    def test_init(self):
        """test if Ant is correctly initialized"""
        assert self.ant.alive is True
        assert self.ant.age == 0
        assert self.ant.location == [10, 10]

    def test_die(self):
        """check if ants die if told so"""
        assert self.ant.alive is True
        self.ant.die()
        assert self.ant.alive is False
        self.ant.alive = True

    def test_get_older(self):
        """check if ants age the right way and die if they age 101 times"""
        assert self.ant.age == 0
        for age in range(1, 101):
            self.ant.get_older(self.field)
            assert self.ant.age == age
            assert self.ant.alive is True
        self.ant.get_older(self.field)
        assert self.ant.alive is False
        self.ant.alive = True
        self.ant.age = 0

    def test_move(self):
        """test if ants move in the right direction and age afterwards"""
        foods = [objects.Food([0, 0])]
        ant2 = objects.Ant()
        ant2.location = [0, 0]
        hive = objects.Hive([12, 10])
        ants = [self.ant, ant2]
        self.ant.move(ants, foods, hive, self.field)
        assert self.ant.age == 1
        assert self.ant.next == [9, 9]
        self.ant.has_food = True
        self.ant.move(ants, foods, hive, self.field)
        assert self.ant.age == 2
        assert self.ant.next == [11, 10]

    def test_ant_names(self):
        """test if Ant names are requested correctly"""
        if self.ant.names:
            raise ValueError
        self.ant.get_ant_names()
        assert isinstance(self.ant.names, list)
        assert len(self.ant.names) == 40
        assert self.ant.name is None
        self.ant.set_name()
        assert self.ant.name is not None


class TestFood(unittest.TestCase):
    """testing class food"""
    food = objects.Food()

    def test_food(self):
        """test all important functions"""
        self.food.amount = 20
        self.food.location = [1, 2]
        self.food.nom()
        assert self.food.amount == 19
        assert self.food.get_x() == self.food.location[0]


class TestUtils(unittest.TestCase):
    """test utils"""


class TestController(unittest.TestCase):
    """test controller"""


if __name__ == "__main__":
    unittest.main()
