# -*- coding: utf-8 -*-
"""
Created on Thu Oct  20 10:13:43 2019

@author: ElJocho
"""

from math import sqrt
import numpy as np


def get_distance(vector):
    """get distance from self to goal"""
    x_coord, y_coord = vector
    return sqrt(x_coord * x_coord + y_coord * y_coord)


def linear_weight(dist, field):
    """weight a vector with a linear function"""
    return 1 - dist / sqrt((field.size[0] * field.size[1]) * 2)


def bell_weight(dist):
    """weight a vector with a bell weight function"""
    max_smell_distance = 2
    min_smell_distance = 1.5  # ants that are next to each other dont run towards each other
    if max_smell_distance > dist > min_smell_distance:
        weight = (1 - (dist / max_smell_distance) ** 2) ** 2
    else:
        weight = 0
    return weight


def normalize(vect, distance):
    """normalize vector"""
    np_vect = np.asarray(vect)
    return np_vect / distance
