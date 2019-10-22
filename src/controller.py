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
import src.errors as err
from typing import Tuple
import json


def load_input():
    with open("settings.txt") as path:
        settings = json.load(path)
    test_input(settings)
    return settings


def create_field(size: int) -> fld.field:
    """
    create the playing board for a run

    Parameters
    ----------
    size : int
        Sets how many columns and rows make up the playing board. Since field is quadratic, size can be an integer.

    Returns
    -------
    field : field
        Instance of class Field.
    """
    field = fld.field(size)
    return field


def create_hive(field: fld.field) -> objects.hive:
    """
    create the ant-hive. It's location is always in the bottom left corner (after animation flips board).

    Parameters
    ----------
    field : field
        playing board used to get field size and to mark ant-hive after creation.

    Returns
    -------
    hive : hive
        Instance of class hive with random location in bottom left corner
    """
    left_bot = field.size[0] // 4
    hive = objects.hive([rdm.randint(0, left_bot), rdm.randint(0, left_bot)])
    field.grid[hive.getX(), hive.getY()] = field.hive
    return hive


def create_ants(amount: int, max_age: int) -> list:
    """
    create all starting ants with names and locations.

    Parameters
    ----------
    amount : int
        amount of starting ants

    max_age : int
        number of turns an ant is alive

    Returns
    -------
    ants: list
        all active Instances of class ant in a list
    """
    ants = []
    objects.ant.get_ant_names()
    for counter in range(0, amount):
        age = rdm.randint(0, max_age//5)  # starting ants start at a low but random age so they don't die synchronous
        ant = objects.ant(max_age, age)
        ant.setName()
        ants.append(ant)
    return ants


def create_food(field: fld.field) -> objects.food:
    """
    create an instance of class food with location and marks newly created instance in field.

    Parameters
    ----------
    field : field
        playing board used to mark location of food

    Returns
    -------
    ants: list
        all active Instances of class ant in a list
    """
    food = objects.food()
    food.location = random_loc(field)
    field.grid[food.getX(), food.getY()] = field.food
    return food


def next_step(ants: list, field: fld.field, foods: list, hive: objects.hive) -> Tuple[list, list]:
    """
    coordinates all needed changes to the field and objects during one time step.

    Parameters
    ----------
    ants : list
        a list containing all active ants

    field : field
        playing board which is altered during the step

    foods : list
        a list containing all active foods

    hive : hive

    Returns
    -------
    ants: list
        all active Instances of class ant in a list
    """
    # every ant declares its desired turn and takes, or puts down, food. Ants also get older, and can die.
    for ant in ants:
        ant.move(ants, foods, hive, field)
    # if any ant took the last piece of food, this food must be deleted now
    foods = [food for food in foods if food.amount > 0]
    # chance for a new food to appear every step
    if 80 / rdm.randint(1, 80) == 1:
        foods.append(create_food(field))
    # any dead ants (which died of old age) will not be tracked anymore
    ants = [ant for ant in ants if ant.alive is True]
    # check if desired locations for ants overlap, saves new locations into ant instances
    collision_check(ants, field)
    # place all ants on the field
    locate_ants(ants, field)
    # check if number of alive ants and number of ants on field are equal
    assert field.count_ants() == len(ants), "not equal"
    # if the hive is not currently occupied by an ant and has enough food and hive is off cooldown: spawn new ant
    if hive.is_ready() and hive.is_free(ants, field):
        ants = hive.spawn_ant(ants, field)
        hive.reset_cooldown()
    # put hive on the map if locations is not occupied by any ant
    hive.is_free(ants, field)
    # put foods on the map if location is not occupied by any ant
    for food in foods:
        food.is_free(ants, field)
    # save current state of playing board to a list which is used to animate mp4
    field.maps.append(field.getFrame())
    # return currently active ants and food
    return ants, foods


def random_loc(field: fld.field) -> list:
    """
    create a set of coordinates which indicate a location that is unoccupied and random

    Parameters
    ----------
    field : field
        playing board which is used to check if the location is unoccupied

    Returns
    -------
    location : list
        unoccupied location
    """
    is_blocked = True
    while is_blocked:
        location = [rdm.randint(0, field.size[0] - 1),
                    rdm.randint(0, field.size[1] - 1)]
        if field.checkCell(location) == field.free:
            is_blocked = False
    return location


def place_ants(ants: list, field: fld.field):
    """
    give starting ants location and place them on field

    Parameters
    ----------
    ants : list
        list of active ants

    field : field
        playing board on which ants are placed
    """
    for ant in ants:
        ant.location = random_loc(field)
        field.grid[ant.getX(), ant.getY()] = field.ant
    field.maps.append(field.getFrame())


def locate_ants(ants: list, field: fld.field):
    """
    place ants on the map on their locations if it is not already used by any other ant.

    Parameters
    ----------
    ants : list
        list of active ants

    field : field
        playing board on which ants are placed
    """
    used = []
    for ant in ants:
        if ant.location not in used:
            field.grid[ant.getX(), ant.getY()] = field.ant
            used.append(ant.location)
        else:
            raise


def collision_check(ants: list, field: fld.field):
    """
    checks if multiple ants want the same location or if ants would stay still for a turn. If that is the case, the ants
    move to a random spot next to them else they move to their desired location.

    Parameters
    ----------
    ants : list
        all active ants

    field : field
        playing board on which ant location is changed to new location after step
    """
    locked = []  # locations which are occupied by an ant after a step are locked and can't be accessed by other ants

    def lock_move(ant: objects.ant, location: list):
        """change ant location, mark ant as already moved and lock new location"""
        if location in locked:
            raise err.MovementError
        ant.location = location
        ant.moved = True
        locked.append(location)

    def trickle_down(ants: list):
        """
        checks for all unmoved ants if its target location is locked. if it detects a movement it checks ants again,
        until all ants in list have either moved or have free desired locations
        """
        detect_movement = False
        while detect_movement is not True:
            for ant in ants:
                if ant.moved is False and ant.next in locked:
                    detect_movement = True
                    random_walk(ant)

    def random_walk(ant: objects.ant):
        """ant moves to a random free spot next to itself"""
        def is_valid(number: int) -> bool:
            """check if number is at least 0 and at maximum the fields size. Dodges IndexErrors"""
            if number < 0 or number >= field.size[0]:
                return False
            else:
                return True

        def check_if_free(x: int, y: int, valid_locations: list):
            """checks if location is unused and valid. If both applies, location is considered a valid location."""
            if [x, y] not in locked and (is_valid(x) and is_valid(y)):
                valid_locations.append([x, y])

        valid_locations = []  # all potential cells/locations
        up = ant.getX() - 1
        down = ant.getX() + 1
        left = ant.getY() - 1
        right = ant.getY() + 1
        # check all 8 neighboring cells
        check_if_free(ant.getX(), left, valid_locations)
        check_if_free(ant.getX(), right, valid_locations)
        check_if_free(up, left, valid_locations)
        check_if_free(down, left, valid_locations)
        check_if_free(up, right, valid_locations)
        check_if_free(down, right, valid_locations)
        check_if_free(up, ant.getY(), valid_locations)
        check_if_free(down, ant.getY(), valid_locations)

        # randomly lock one free spot
        if len(valid_locations) != 0:
            lock_move(ant, valid_locations[rdm.randint(0, len(valid_locations) - 1)])
        # if there are no free spots, try ants own location
        elif ant.location not in locked:
            lock_move(ant, ant.location)
        # if neighboring spot is free, and own location is occupied too, raise MovementError
        else:
            raise err.MovementError

    for ant in ants:
        # mark all current locations of ants as empty
        field.grid[ant.getX(), ant.getY()] = field.free
        # move all ants which would stay still
        if ant.location == ant.next and ant.moved is False:
            random_walk(ant)

    trickle_down(ants)

    # move all unblocked ants
    for ant in ants:
        if ant.moved is False and ant.next not in locked:
            lock_move(ant, ant.next)

    trickle_down(ants)

    [ant.unmove() for ant in ants]  # reset ant.moved


def create_animation(field: fld.field):
    """
    coordinates creation of animation. writes resulting mp4 to results/ant.mp4

    Parameters
    ----------
    field : field
        field contains all steps in field.maps
    """
    anim, writer = field.make_animation()
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, '..', 'results')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, 'ant.mp4')
    anim.save(path, writer=writer)


def print_stats(hive: objects.hive, ants: list):
    """
    writes some stats into the console which give a quick impression of a run before it is animated.

    Parameters
    ----------
    hive : hive
        used to print out how many food was left in storage when simulation ended

    ants : list
        all active ants. Number of remaining ants and their names get printed
    """
    print("collected food: {}".format(hive.food))
    print("surviving ants: {}".format(len(ants)))
    [print(ant.name) for ant in ants]


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

    def test_value(value, maxvalue: int):  # value not specified so assert can make more accurate Error output
        """test if value in valid range and an integer"""
        assert type(value) == int, "value is not integer"
        assert value > 0, "value is less than 1"
        assert value <= maxvalue, "value is too big"

    for key, value in settings.items():
        try:
            test_value(value, max_value[key])
        except AssertionError as e:
            print("-" * 60)
            print("Error in {}".format(key))
            print(e)
            print("please enter valid values in the settings.txt file")
            print("valid range: 1 - {}".format(max_value[key]))
            print("-" * 60)
            sys.exit()
