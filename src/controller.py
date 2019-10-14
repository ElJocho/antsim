# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:47:02 2019

@author: ElJocho
"""
import src.field as fld
import src.objects as objects
import random as rdm
import os
import sys


def create_field(size):
    field = fld.field(size)
    return field


def create_hive(field):
    left_bot = field.size[0] // 4
    hive = objects.hive([rdm.randint(0, left_bot), rdm.randint(0, left_bot)])
    field.grid[hive.getX(), hive.getY()] = field.hive
    return hive


def create_ants(count, max_age):
    ants = []
    names = objects.get_ant_names()

    for counter in range(0, count):
        age = rdm.randint(0,10)
        ant = objects.ant(max_age, age)
        ant.name = names[counter]
        ants.append(ant)
    return ants


def create_food(field):
    food = objects.food()
    food.location = random_loc(field)
    field.grid[food.getX(), food.getY()] = field.food
    return food


def next_step(ants, field, foods, hive):
    for ant in ants:
        ant.move(ants, foods, hive, field)
    foods = [food for food in foods if food.amount > 0]
    if 80/rdm.randint(1,80) == 1:
        foods.append(create_food(field))
    ants = [ant for ant in ants if ant.alive is True]
    objects.collision_check(ants, field)
    locate_ants(ants, field)
    assert field.count_ants() == len(ants), "not equal"
    if hive.is_ready() and hive.is_free(ants, field):
        ants = hive.spawn_ant(ants, field)

    hive.is_free(ants,field)
    for food in foods:
        food.is_free(ants, field)
    field.maps.append(field.getFrame())
    return ants, foods


def random_loc(field):
    is_blocked = True
    while is_blocked:
        location = [rdm.randint(0, field.size[0]-1),
                    rdm.randint(0, field.size[1]-1)]
        if field.checkCell(location) == field.free:
            is_blocked = False
    return location


def place_ants(ants, field):
    for ant in ants:
        ant.location = random_loc(field)
        field.grid[ant.getX(), ant.getY()] = field.ant
    field.maps.append(field.getFrame())


def locate_ants(ants, field):
    used = []
    for ant in ants:
        if ant.location not in used:
            field.grid[ant.getX(), ant.getY()] = field.ant
            used.append(ant.location)

def create_animation(field):
    anim, writer = field.make_animation()
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, '..', 'results')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, 'ant.mp4')
    anim.save(path, writer=writer)


def print_stats(hive, ants):
    print("collected food: {}".format(hive.food))
    print("surviving ants: {}".format(len(ants)))
    [print(ant.name) for ant in ants]


def test_input(settings):
    max_value = {
                "number_of_turns": 10000,
                "number_of_ants": 40,
                "field_size": 1000,
                "maximum_age": 100000000000000000
                }

    def test(value, maxvalue=None):
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
            print("-"*60)
            print("Error in {}".format(key))
            print(e)
            print("please enter valid values in the settings.txt file")
            print("valid range: 1 - {}".format(max_value[key]))
            print("-"*60)
            sys.exit()
