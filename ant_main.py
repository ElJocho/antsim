# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:09:33 2019

@author: ElJocho
"""
import src.controller as ctr

def main():
    field = ctr.create_field()
    active_ants = ctr.create_ants(10)
    field = ctr.place_ants(active_ants, field)
    
    for step in range(0, 81):
        ctr.next_step(active_ants)
    
        
main()