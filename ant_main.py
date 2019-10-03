# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:09:33 2019

@author: ElJocho
"""
import src.controller as ctr

def main():
    field = ctr.create_field()
    ants = ctr.create_ants()

    for step in range(0, 80):
        ctr.next_step()
