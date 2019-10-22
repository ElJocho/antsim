# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:47:53 2019

@author: ElJocho
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


class field():
    free = 0
    ant = 1
    food = 2
    hive = 3

    def __init__(self, size):
        self.size = [size, size]
        self.grid = np.zeros(self.size)
        self.maps = []

    def plot(self):
        plot_size = self.size
        plt.figure(figsize=(10, 10))
        ax = plt.axes(xlim=(0, plot_size[1]), ylim=(0, plot_size[0]))
        a = self.maps[0]
        ax.imshow(a, interpolation='none', vmin=0, vmax=2, cmap='brg_r')
        plt.show()

    def checkCell(self, cell):
        try:
            self.is_valid(cell)
        except IndexError:
            print("input cell parameter out of boundaries: {}".format(cell))
            raise IndexError
        return self.grid[cell[0], cell[1]]

    def setCell(self, cell, value):
        try:
            self.is_valid(cell)
            self.is_valid(value)
        except ValueError:
            print("invalid Value in setCell value {}".format(value))
            raise ValueError
        except IndexError:
            print("invalid coordinates in setCell {}".format(cell))
            raise IndexError
        self.grid[cell[0], cell[1]] = value

    def is_valid(self, data):
        if type(data) == list:
            try:
                assert len(data) == 2
                assert data[0] < self.size[0] and data[0] >= 0
                assert data[1] < self.size[1] and data[1] >= 0
            except AssertionError:
                raise IndexError
        if type(data) == int:
            try:
                assert data <= 1
                assert data >= 0
            except AssertionError:
                raise ValueError

    def count_ants(self):
        return np.count_nonzero(self.grid == field.ant)

    def getFrame(self):
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
        ax = plt.axes(xlim=(-0.5, plot_size[1]), ylim=(-0.5, plot_size[0]))
        a = self.maps[0]
        im = ax.imshow(a, interpolation='none', vmin=0, vmax=3,
                       cmap='brg_r')

        # initialization function: plot the background of each frame
        def init():
            im.set_data(np.zeros(plot_size))
            return [im]

        # animation function.  This is called sequentially
        def animate(i):
            im.set_array(self.maps[i])
            return [im]

        # call the animator.
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=n_iterations,
                                       interval=500)
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='ElJocho'), bitrate=-1)

        return anim, writer
