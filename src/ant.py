# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:39:07 2019

@author: ElJocho
"""


class ant():
    def __init__(self):
        self.alive = True
        self.age = 0
        self.location = None

    def move(self):
        if self.alive is True:
            pass  # move
            
            self.getOlder()

    def getOlder(self):
        if self.age < 79:
            self.age += 1
        else:
            self.die()

    def die(self):
        self.alive = False
