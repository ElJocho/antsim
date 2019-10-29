# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:47:53 2019

@author: ElJocho
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


class Field:
    """
    provides functions to build and manage a grid which is used for animating the Ant sim.
    """
    FREE = 0
    ANT = 1
    FOOD = 2
    HIVE = 3

    def __init__(self, size: int = 50):
        self.size = [size, size]
        self.grid = np.zeros(self.size)
        self.maps = []

    def plot(self):
        """unused in final animation process, but useful for testing. Plot current state of grid."""
        plot_size = self.size
        plt.figure(figsize=(10, 10))
        axes = plt.axes(xlim=(0, plot_size[1]), ylim=(0, plot_size[0]))
        start = self.maps[0]
        axes.imshow(start, interpolation='none', vmin=0, vmax=2, cmap='brg_r')
        plt.show()

    def check_cell(self, cell: list):
        """return value of Field specified through coordinates in cell"""
        try:
            self.is_valid(cell)
        except IndexError:
            print("input cell parameter out of boundaries: {}".format(cell))
            raise IndexError
        return self.grid[cell[0], cell[1]]

    def set_cell(self, cell: list, value: int):
        """initiate test if a cell is valid. If it is valid, set cell: list to value: int"""
        try:
            self.is_valid(cell)
            self.is_valid(value)
        except ValueError:
            print("invalid Value in set_cell value {}".format(value))
            raise ValueError
        except IndexError:
            print("invalid coordinates in set_cell {}".format(cell))
            raise IndexError
        self.grid[cell[0], cell[1]] = value

    def is_valid(self, data):
        """raises Errors if data is not valid. data can be int or list."""
        if isinstance(data, list):
            try:
                assert len(data) == 2
                assert self.size[0] > data[0] >= 0
                assert self.size[1] > data[1] >= 0
            except AssertionError:
                raise IndexError
        if isinstance(data, int):
            try:
                assert data <= 3
                assert data >= 0
            except AssertionError:
                raise ValueError

    def count_ants(self):
        """returns how many ants are currently on the field"""
        return np.count_nonzero(self.grid == Field.ANT)

    def get_frame(self):
        """get a copy of the current field"""
        return np.copy(self.grid)

    def make_animation(self):
        """
        Creates an animation
        param: maps is a list of numpy arrays at different time steps
        """
        plot_size = self.size
        n_iterations = len(self.maps)

        # set up the figure, the axis, and the plot element we want to animate
        fig = plt.figure(figsize=(15, 15))
        axes = plt.axes(xlim=(-0.5, plot_size[1]), ylim=(-0.5, plot_size[0]))
        start = self.maps[0]
        image = axes.imshow(start, interpolation='none', vmin=0, vmax=3,
                            cmap='brg_r')

        # initialization function: plot the background of each frame
        def init():
            image.set_data(np.zeros(plot_size))
            return [image]

        # animation function.  This is called sequentially
        def animate(i):
            image.set_array(self.maps[i])
            return [image]

        # call the animator.
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=n_iterations,
                                       interval=500)
        writer = animation.writers['ffmpeg']
        writer = writer(fps=15, metadata=dict(artist='ElJocho'), bitrate=-1)

        return anim, writer
