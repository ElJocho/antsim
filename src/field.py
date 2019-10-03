# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:47:53 2019

@author: ElJocho
"""

import numpy as np
import matplotlib.pyplot as plt


class field():
    free = 0
    ant = 1
    food = 2

    def __init__(self):
        self.size = 50 * 50
        self.grid = np.zeros([50, 50])
        self.grid[49, 49] = self.food

    def plot(self, ant_locations):
        plt.figure(figsize=(10, 10))
        plt.imshow(self.grid)
        plt.gray()
        plt.show()

    def checkCell(self, cell):
        try:
            self.is_valid(cell)
        except AssertionError:
            print("input cell parameter out of boundaries: {}".format(cell))
            raise ValueError
        return self.grid[cell[0], cell[1]]

    def setCell(self, cell, value):
        try:
            self.is_valid(cell)
            self.is_valid(value)
        except AssertionError:
            print("invalid input in setCell. Cell {}, value {}".format(cell,
                                                                       value))
            raise ValueError
        self.grid[cell[0], cell[1]] = value

    def is_valid(self, data):
        if type(data) == list:
            assert len(data) == 2
            assert data[0] <= 49 and data[0] >= 0
            assert data[1] <= 49 and data[1] >= 0
        if type(data) == int:
            assert data <= 1
            assert data >= 0
