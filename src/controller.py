# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:47:02 2019

@author: ElJocho
"""
import src.field as fld
import src.ant as ant_
import random as rdm


def create_field():
    field = fld.field()
    return field


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


def create_ants(count):
    try:
        assert count <= 40
        assert count >= 0
    except AssertionError:
        raise ValueError("Invalid Input, enter a value between 0 and 40")
    ants = []
    names = ant_.get_ant_names()

    for counter in range(0, count):
        ant = ant_.ant()
        ant.name = names[counter]
        ants.append(ant)
    return ants


def next_step(ants):
    for ant in ants:
        ant.move()


def place_ants(ants, field):
    for ant in ants:
        is_blocked = True
        while is_blocked:
            ant.location = [rdm.randint(0, 49), rdm.randint(0, 49)]
            if field.checkCell(ant.location) == field.free:
                field.setCell(ant.location, field.ant)
                is_blocked = False
                
