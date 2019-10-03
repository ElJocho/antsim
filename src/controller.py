# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:47:02 2019

@author: ElJocho
"""
import src.field as fld
import src.ant as ant_
import random as rdm

def create_field():
    field = fld.field()
    return field


def create_ants(count):
    ants = []
    names = ant_.get_ant_names()

    for counter in range(0, count):
        ant = ant_.ant()
        ant.name = names[counter]
        ants.append(ant)
    return ants


def next_step(ants):
    print("-"*10)
    for ant in ants:
        print(ant.age)
        ant.move()
    print("-"*10)


def place_ants(ants, field):
    is_blocked = True
    for ant in ants:
        while is_blocked:
            ant.location = [rdm.randint(0, 49), rdm.randint(0, 49)]
            
            if field.cellIsFree(ant.location) == field.free:
                field.setCell(ant.location, field.ant)
                is_blocked = False
    
