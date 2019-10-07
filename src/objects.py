# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:39:07 2019

@author: ElJocho
"""
import requests
from math import sqrt
import numpy as np


class ant():
    hive_location = [15, 15]

    def __init__(self, max_age):
        self.alive = True
        self.age = 0
        self.location = None
        self.name = None
        self.hasFood = False
        self.maxAge = max_age

    def getOlder(self):
        if self.age < self.maxAge:
            self.age += 1
        else:
            self.die()

    def die(self):
        self.alive = False

    def getX(self):
        return self.location[0]

    def getY(self):
        return self.location[1]

    def move(self, ants, foods):
        influences = []

        def final_direction():
            sum_weight = 0.
            weighted_x = 0.
            weighted_y = 0.
            for entry in influences:
                sum_weight += entry[0]
                weighted_x += entry[0]*entry[1][0]
                weighted_y += entry[0]*entry[1][1]
            x = weighted_x / sum_weight
            y = weighted_y / sum_weight
            return x, y

        def normalize(vect, distance):
            np_vect = np.asarray(vect)
            return np_vect/distance

        def get_vector(self, goal):
            rel_x = goal[0] - self.getX()
            rel_y = goal[1] - self.getY()
            return rel_x, rel_y

        def get_distance(vector):
            x, y = vector
            return sqrt(x * x + y * y)

        def linear_weight(dist):
            return 1 - dist/sqrt((50*50)*2)

        def towards_food(self, food):
            vect = get_vector(self, food)
            dist = get_distance(get_vector(self, food))
            if dist == 0:
                return 0
            normed = normalize(vect, dist)
            weight = linear_weight(dist)
            influences.append((weight, normed))

        def towards_hive(self):
            pass

        def towards_ant(self, ant):
            pass

        if self.alive is True:
            if self.hasFood is True:
                towards_hive(self)
            else:
                for food in foods:
                    if self.location == food.location:
                        self.die()
                    towards_food(self, food.location)

            for ant in ants:
                if ant.name != self.name:
                    towards_ant(self, ant.location)

            if len(influences) == 0:
                return 0
            x, y = final_direction()

            if x >= 0.5:
                self.location[0] += 1
            elif x <= -0.5:
                self.location[0] -= 1
            if y >= 0.5:
                self.location[1] += 1
            elif y <= -0.5:
                self.location[1] -= 1
            self.getOlder()


def get_ant_names():
    url = """http://www.babynamewizard.com/baby-name/
             advanced-name-finder/results?start=Ant"""
    url = url.replace("\n", "").replace(" ", "")  # replace whitespaces
    data = requests.get(url)

    text = data.text
    # remove everything except lines with wanted content
    nametext = text[text.find("content-content"):text.find("/content-content")]
    lines = nametext.splitlines()
    names = []
    for line in lines:
        if line.find("girl/") != -1:
            name = line[line.find("girl/")+5:line.find("\" class")]
        elif line.find("boy/") != -1:
            name = line[line.find("boy/")+4:line.find("\" class")]
        else:
            continue
        if len(name) > 0:
            names.append(name)
    names.append("antifa")
    names.append("antman")
    return names


class food():
    def __init__(self, amount=None, location=None):
        self.amount = amount
        self.location = location

    def getX(self):
        return self.location[0]

    def getY(self):
        return self.location[1]

    def changeAmount(self, x):
        self.amount = self.amount + x
