# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:47:53 2019

@author: ElJocho
"""

import numpy as np
import matplotlib.pyplot as plt

class field():
    def __init__(self):
        self.size = 50 * 50
        self.grid = np.zeros([50, 50])
        self.grid[49, 49] = 2
    
    def plot(self):
        plt.figure(figsize=(10, 10))
        plt.imshow(self.grid)
        plt.gray()
        plt.show()

