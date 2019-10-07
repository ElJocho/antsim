# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:09:33 2019

@author: ElJocho
"""
import src.controller as ctr
import json

# CONFIG FILLLLEEEEEEEEEEEEEEE!!!!!!


def load_input():
    with open("settings.txt") as path:
        settings = json.load(path)
    ctr.test_input(settings)
    return settings


def main():
    settings = load_input()

    # setup starting conditions
    field = ctr.create_field(settings["field_size"])
    active_ants = ctr.create_ants(settings["number_of_ants"],
                                  settings["maximum_age"])

    active_food = ctr.create_food(field)
    ctr.place_ants(active_ants, field)

    # execute certain number of turns
    for step in range(0, settings["number_of_turns"]):
        ctr.next_step(active_ants, field, active_food)

    # create an animation and save the result to results/ants.mp4
    ctr.create_animation(field)
    print("animation saved to results/ants.mp4")


main()
