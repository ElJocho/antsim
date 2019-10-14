# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:09:33 2019

@author: ElJocho
"""
import src.controller as ctr
import json
import sys
import src.errors as err

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
    hive = ctr.create_hive(field)
    active_ants = ctr.create_ants(settings["number_of_ants"],
                                  settings["maximum_age"])

    foods = [ctr.create_food(field)]
    ctr.place_ants(active_ants, field)

    # execute certain number of turns
    n = settings["number_of_turns"]
    for step in range(0, n):
        if (step % 10 == 0 and step != 0) or step == n-1:
            sys.stdout.write("\r{:3.2f}%".format(step/(n-1)*100))
        active_ants, foods = ctr.next_step(active_ants, field, foods, hive)

    # create an animation and save the result to results/ants.mp4
    print("\nstarting to generate mp4, have some stats for now")
    ctr.print_stats(hive, active_ants)
    ctr.create_animation(field)
    print("\nanimation saved to results/ants.mp4")


if __name__ == "__main__":
    not_finished = True
    while not_finished:
        try:
            main()
            not_finished = False
        except err.MovementError:
            print("\nran into Error, happens if ant cant make any valid move.")
            print("restarting simulation")
