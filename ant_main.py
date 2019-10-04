# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:09:33 2019

@author: ElJocho
"""
import src.controller as ctr
import sys


def main():
    try:
        ant_count = sys.argv[1]
        turn_count = sys.argv[2]
    except IndexError:
        ant_count, turn_count = None, None

    ant_count, turn_count = ctr.test_input(ant_count, turn_count)

    field = ctr.create_field()
    active_ants = ctr.create_ants(ant_count)
    ctr.place_ants(active_ants, field)

    for step in range(0, turn_count):
        ctr.next_step(active_ants, field)

    ctr.create_animation(field)


main()
