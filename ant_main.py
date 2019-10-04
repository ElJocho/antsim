# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:09:33 2019

@author: ElJocho
"""
import src.controller as ctr
import sys


# CONFIG FILLLLEEEEEEEEEEEEEEE!!!!!!

def load_input():
    try:
        ant_count = sys.argv[1]
        turn_count = sys.argv[2]
    except IndexError:
        ant_count, turn_count = None, None
    finally:
        return ant_count, turn_count


def main():
    # try to load and validate optional inputs
    ant_count, turn_count = load_input()
    ant_count, turn_count = ctr.test_input(ant_count, turn_count)

    # setup starting conditions
    field = ctr.create_field()
    active_ants = ctr.create_ants(ant_count)
    active_food = ctr.create_food(field)
    ctr.place_ants(active_ants, field)

    # execute certain number of turns
    for step in range(0, turn_count):
        ctr.next_step(active_ants, field, active_food)

    # create an animation and save the result to results/ants.mp4
    ctr.create_animation(field)
    print("animation saved to results/ants.mp4")


main()
