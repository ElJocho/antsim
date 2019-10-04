# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:47:02 2019

@author: ElJocho
"""
import src.field as fld
import src.objects as objects
import random as rdm
import os


def create_field():
    field = fld.field()
    return field


def create_ants(count):
    ants = []
    names = objects.get_ant_names()

    for counter in range(0, count):
        ant = objects.ant()
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


def test_input(ant_count, turn_count):

    def set_value(value, valid_count):
        if value is None:
            print("valid range: {}".format(valid_count))
            value = input()
        try:
            value = int(value)
            assert value >= valid_count[0]
            assert value <= valid_count[1]
        except AssertionError:
            value = None
            print("number out of range, please try again")
            value = set_value(value, valid_count)
        except ValueError:
            value = None
            print("input must be an number")
            value = set_value(value, valid_count)
        else:
            print("valid Input: {}".format(value))
        finally:
            return value
    valid_ant_count = [0, 40]
    valid_turn_count = [1, 100]

    if ant_count is None or turn_count is None:
        ant_count, turn_count = None, None
        print("please enter number of spawning ants, then number of turns\n")

    ant_count = set_value(ant_count, valid_ant_count)
    turn_count = set_value(turn_count, valid_turn_count)
    return ant_count, turn_count
