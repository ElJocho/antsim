# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:09:33 2019

@author: ElJocho
"""
import sys
import src.controller as ctr
import src.errors as err


def main():
    """
    initiates main steps to execute Ant sim
    input:
    settings.txt
        4 variables which set the starting conditions and how many turns ants survive.
    output:
    statistics
          some statistics on which ants survived, and how many Food is left in storage
    results/ants.mp4
        mp4 video which animates all steps
    """
    print("\nloading settings.txt and setting up starting conditions")
    settings = ctr.load_input()

    # setup starting conditions
    field = ctr.create_field(settings["field_size"])
    hive = ctr.create_hive(field)
    foods = [ctr.create_food(field)]
    active_ants = ctr.create_ants(settings["number_of_ants"],
                                  settings["maximum_age"],
                                  field)
    print("starting to simulate time steps")
    # execute certain number of turns
    nof = settings["number_of_turns"]
    for step in range(0, nof):
        if (step % 10 == 0 and step != 0) or step == nof-1:
            sys.stdout.write("\r{:3.2f}% done".format(step/(nof-1)*100))
        active_ants, foods = ctr.next_step(active_ants, field, foods, hive)

    # create an animation and save the result to results/ants.mp4
    print("\n\nstarting to generate mp4, have some stats for now")
    ctr.print_stats(hive, active_ants)
    ctr.create_animation(field)
    print("\nanimation saved to results/ants.mp4")


if __name__ == "__main__":
    # repeats main till ant valid run occurs.
    # Runs can be invalid if an Ant doesnt have any location to which it can move.
    NOT_FINISHED = True  # pylint thought this is constant idk why
    while NOT_FINISHED:
        try:
            main()
            NOT_FINISHED = False
        except err.MovementError:
            print("\nran into Error, happens if Ant cant make any valid move.")
            print("restarting simulation")
