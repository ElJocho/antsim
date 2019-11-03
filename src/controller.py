# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:47:02 2019

@author: ElJocho
"""
import random as rdm
import os
import sys
from typing import Tuple
import json
import src.field as fld
import src.objects as objects
import src.errors as err
import src.utils as utils


def load_input():
    """loads settings from file settings.txt"""
    with open("settings.txt") as path:
        settings = json.load(path)
    test_input(settings)
    return settings


def create_field(size: int) -> fld.Field:
    """
    create the playing board for a run

    Parameters
    ----------
    size : int
        Sets how many columns and rows make up the playing board.

    Returns
    -------
    field : Field
        Instance of class Field.
    """
    field = fld.Field(size)
    return field


def create_hive(field: fld.Field) -> objects.Hive:
    """
    create the Ant-Hive. It's location is always in the bottom left corner
    (after animation flips board).

    Parameters
    ----------
    field : Field
        playing board used to get Field size and to mark Ant-Hive after creation.

    Returns
    -------
    Hive : Hive
        Instance of class Hive with random location in bottom left corner
    """
    left_bot = field.size[0] // 4
    hive = objects.Hive([rdm.randint(0, left_bot), rdm.randint(0, left_bot)])
    field.set_cell(hive.location, field.HIVE)
    return hive


def create_food(field: fld.Field) -> objects.Food:
    """
    create an instance of class Food with location and marks newly created instance in Field.

    Parameters
    ----------
    field : Field
        playing board used to mark location of Food

    Returns
    -------
    ants: list
        all active Instances of class Ant in a list
    """
    food = objects.Food()
    food.location = utils.random_loc(field)
    field.set_cell(food.location, field.FOOD)
    return food


def create_ants(amount: int, max_age: int, field: object) -> list:
    """
    create all starting ants with names and locations.

    Parameters
    ----------
    amount : int
        amount of starting ants

    max_age : int
        number of turns an Ant is alive

    field : Field
        necessairy for place_ants
    Returns
    -------
    ants: list
        all active Instances of class Ant in a list
    """
    ants = []
    objects.Ant.get_ant_names()
    for counter in range(0, amount):
        age = rdm.randint(0, max_age//5)  # ants start at a low, random age for asynchronous death
        ant = objects.Ant(max_age, age)
        ant.set_name()
        ants.append(ant)
    utils.place_ants(ants, field)
    return ants


def next_step(ants: list, field: fld.Field, foods: list, hive: objects.Hive)\
              -> Tuple[list, list]:
    """
    coordinates all needed changes to the Field and objects during one time step.

    Parameters
    ----------
    ants : list
        a list containing all active ants

    field : Field
        playing board which is altered during the step

    foods : list
        a list containing all active foods

    hive : Hive

    Returns
    -------
    ants: list
        all active Instances of class Ant in a list
    """
    # every Ant declares its desired turn. Ants also get older, and can die.
    for ant in ants:
        ant.move(ants, foods, hive, field)
    # any dead ants (which died of old age) will not be tracked anymore
    ants = [ant for ant in ants if ant.alive is True]
    # if any Ant took the last piece of a Food, this Food must be deleted now
    foods = [food for food in foods if food.amount > 0]
    # chance for a new Food to appear every step
    if 80 / rdm.randint(1, 80) == 1:
        foods.append(create_food(field))
    # check if desired locations for ants overlap
    collision_check(ants, field)
    # place all ants on the Field
    utils.locate_ants(ants, field)
    # check if number of alive ants and number of ants on Field are equal
    assert field.count_ants() == len(ants), "not equal"
    # if the Hive is not currently occupied by an Ant try spawning new Ant
    if hive.is_ready() and hive.is_free(ants, field):
        ants = hive.spawn_ant(ants, field)
        hive.reset_cooldown()
    # put Hive on the map if locations is not occupied by any Ant
    hive.is_free(ants, field)
    # put foods on the map if location is not occupied by any Ant
    for food in foods:
        food.is_free(ants, field)
    # save current state of playing board to a list which is used to animate mp4
    assert field.count_ants() == len(ants), "not equal"
    field.maps.append(field.get_frame())
    # return currently active ants and Food
    return ants, foods


def collision_check(ants: list, field: fld.Field):
    """
    checks if multiple ants want the same location or if ants would stay still for a turn.
    If that is the case, the ants move to a random spot next to them else they move
    to their desired location.

    Parameters
    ----------
    ants : list
        all active ants

    field : Field
        playing board on which Ant location is changed to new location after step
    """
    # locations which are occupied by an Ant after a step are locked for other ants
    locked = []

    def lock_move(ant: objects.Ant, location: list):
        """change Ant location, mark Ant as already moved and lock new location"""
        if location in locked:
            raise err.MovementError
        ant.location = location
        ant.moved = True
        locked.append(location)

    def trickle_down(ants: list):
        """
        checks for all unmoved ants if its target location is locked.
        If it detects a movement it checks ants again,
        until all ants in list have either moved or have free desired locations
        """
        detect_movement = False
        while detect_movement is not True:
            detect_movement = True
            for ant in ants:
                if ant.moved is False and ant.next in locked:
                    detect_movement = False
                    random_walk(ant)

    def random_walk(ant: objects.Ant):
        """Ant moves to a random free spot next to itself"""
        def is_valid(number: int) -> bool:
            """
            check if number is at least 0 and at maximum the fields size.
            Dodges IndexErrors
            """
            if number < 0 or number >= field.size[0]:
                return False
            return True

        def check_if_free(x_coord: int, y_coord: int, valid_locations: list):
            """
            checks if location is unused and valid.
            If both applies, location is considered a valid location.
            """
            if [x_coord, y_coord] not in locked and (is_valid(x_coord) and is_valid(y_coord)):
                valid_locations.append([x_coord, y_coord])

        valid_locations = []  # all potential cells/locations
        up = ant.get_x() - 1
        down = ant.get_x() + 1
        left = ant.get_y() - 1
        right = ant.get_y() + 1
        # check all 8 neighboring cells
        check_if_free(ant.get_x(), left, valid_locations)
        check_if_free(ant.get_x(), right, valid_locations)
        check_if_free(up, left, valid_locations)
        check_if_free(down, left, valid_locations)
        check_if_free(up, right, valid_locations)
        check_if_free(down, right, valid_locations)
        check_if_free(up, ant.get_y(), valid_locations)
        check_if_free(down, ant.get_y(), valid_locations)

        # randomly lock one free spot
        if len(valid_locations) >= 1:
            lock_move(ant, valid_locations[rdm.randint(0, len(valid_locations) - 1)])
        # if there are no free spots, try ants own location
        elif ant.location not in locked:
            lock_move(ant, ant.location)
        # if neighboring spot is free, and own location is occupied too, raise MovementError
        else:
            raise err.MovementError

    for ant in ants:
        # mark all current locations of ants as empty
        field.set_cell(ant.location, field.FREE)
        # move all ants which would stay still
        if ant.location == ant.next and ant.moved is False:
            random_walk(ant)

    trickle_down(ants)

    # move all unblocked ants
    for ant in ants:
        if ant.moved is False and ant.next not in locked:
            lock_move(ant, ant.next)

    trickle_down(ants)

    for ant in ants:
        ant.reset_moved()


def print_stats(hive: objects.Hive, ants: list):
    """
    writes some stats into the console which give a quick impression of a run before it is animated.

    Parameters
    ----------
    hive : Hive
        used to print out how many Food was left in storage when simulation ended

    ants : list
        all active ants. Number of remaining ants and their names get printed
    """
    print("collected Food: {}".format(hive.food))
    print("surviving ants: {}".format(len(ants)))
    for ant in ants:
        print(ant.name)


def create_animation(field: fld.Field):
    """
    coordinates creation of animation. writes resulting mp4 to results/Ant.mp4

    Parameters
    ----------
    field : Field
        Field contains all steps in Field.maps
    """
    anim, writer = field.make_animation()
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, '..', 'results')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, 'Ant.mp4')
    anim.save(path, writer=writer)


def test_input(settings: dict):
    """
    tests if input variables in settings file are valid

    Parameters
    ----------
    settings : list
        a list containing all input variables
    """
    max_value = {
        "number_of_turns": 10000,
        "number_of_ants": 1000,
        "field_size": 1000,
        "maximum_age": 100000000000000000
    }

    def test_value(value, maxvalue: int):
        """test if value in valid range and an integer"""
        assert isinstance(value, int), "value is not integer"
        assert value > 0, "value is less than 1"
        assert value <= maxvalue, "value is too big"

    for key, value in settings.items():
        try:
            test_value(value, max_value[key])
        except AssertionError as error:
            print("-" * 60)
            print("Error in {}".format(key))
            print(error)
            print("please enter valid values in the settings.txt file")
            print("valid range: 1 - {}".format(max_value[key]))
            print("-" * 60)
            sys.exit()
