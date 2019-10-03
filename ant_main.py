# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:09:33 2019

@author: ElJocho
"""
import src.controller as ctr

def main(ant_count = None, turn_count = None):
    ant_count, turn_count = ctr.test_input(ant_count, turn_count)

    field = ctr.create_field()
    active_ants = ctr.create_ants(ant_count)
    field = ctr.place_ants(active_ants, field)

    for step in range(0, turn_count):
        ctr.next_step(active_ants)
    
        
main(40, 100)