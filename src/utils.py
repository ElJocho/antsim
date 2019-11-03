# -*- coding: utf-8 -*-
"""
Created on Thu Oct  20 10:13:43 2019

@author: ElJocho
"""


from math import sqrt
import random as rdm

import numpy as np


def get_distance(vector: tuple) -> float:
    """get distance from self to goal"""
    x_coord, y_coord = vector
    return sqrt(x_coord * x_coord + y_coord * y_coord)


def linear_weight(dist: float, field: object) -> float:
    """weight a vector with a linear function"""
    return 1 - dist / sqrt((field.size[0] * field.size[1]) * 2)


def bell_weight(dist: float) -> float:
    """weight a vector with a bell weight function"""
    max_smell_distance = 3.5
    min_smell_distance = 1.5  # ants that are next to each other dont run towards each other
    if max_smell_distance > dist >= min_smell_distance:
        weight = (1 - (dist / max_smell_distance) ** 2) ** 2
    else:
        weight = 0.
    return weight


def normalize(vect: tuple, distance: float) -> np.array:
    """normalize vector"""
    np_vect = np.asarray(vect)
    return np_vect / distance


def random_loc(field: object) -> list:
    """
    create a set of coordinates which indicate a location that is unoccupied and random

    Parameters
    ----------
    field : Field
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
        if field.check_cell(location) == field.FREE:
            is_blocked = False
    return location


def place_ants(ants: list, field: object):
    """
    give starting ants location and place them on Field

    Parameters
    ----------
    ants : list
        list of active ants

    field : Field
        playing board on which ants are placed
    """
    for ant in ants:
        ant.location = random_loc(field)
        field.set_cell(ant.location, field.ANT)
    field.maps.append(field.get_frame())


def locate_ants(ants: list, field: object):
    """
    place ants on the map on their locations.

    Parameters
    ----------
    ants : list
        list of active ants

    field : Field
        playing board on which ants are placed
    """
    for ant in ants:
        field.set_cell(ant.location, field.ANT)
