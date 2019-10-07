# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:47:02 2019

@author: ElJocho
"""
import src.field as fld
import src.objects as objects
import random as rdm
import os


def create_field(size):
    field = fld.field(size)
    return field


def create_ants(count, max_age):
    ants = []
    names = objects.get_ant_names()

    for counter in range(0, count):
        ant = objects.ant(max_age)
        ant.name = names[counter]
        ants.append(ant)
    return ants


def create_food(field):
    food = objects.food()
    food.amount = rdm.randint(5, 20)
    food.location = [49, 49]
    field.grid[food.getX(), food.getY()] = field.food
    return [food]


def next_step(ants, field, food):

    for ant in ants:
        field.grid[ant.getX(), ant.getY()] = 0
        ant.move(ants, food)
        field.grid[ant.getX(), ant.getY()] = 1
    field.maps.append(field.getFrame())


def place_ants(ants, field):
    for ant in ants:
        is_blocked = True
        while is_blocked:
            ant.location = [rdm.randint(0, 49), rdm.randint(0, 49)]
            if field.checkCell(ant.location) == field.free:
                field.setCell(ant.location, field.ant)
                is_blocked = False
    field.maps.append(field.getFrame())


def create_animation(field):
    anim, writer = field.make_animation()
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, '..', 'results')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, 'ant.mp4')
    anim.save(path, writer=writer)


def test_input(settings):
    max_value = {
                "number_of_turns": 10000,
                "number_of_ants": 40,
                "field_size": [1000, 1000],
                "maximum_age": 100000000000000000
                }

    def test(value, maxvalue=None):
        if type(value) == list:
            assert len(value) == 2, "more than 2 values passed"
            [test_value(value[x], maxvalue[x]) for x in range(len(value))]
        else:
            test_value(value, maxvalue)

    def test_value(value, maxvalue):
        assert type(value) == int, "value is not integer"
        assert value > 0, "value is less than 1"
        try:
            assert value <= maxvalue, "value is too big"
        except TypeError:
            pass

    for key, value in settings.items():
        try:
            test(value, max_value[key])
        except AssertionError as e:
            print("Error in {}".format(key))
            print(e)
            exit()
