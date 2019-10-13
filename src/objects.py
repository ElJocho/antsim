# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:39:07 2019

@author: ElJocho
"""
import requests
from math import sqrt
import numpy as np
from copy import deepcopy as dc
import random as rnd

class ant():
    hive_location = [15, 15]

    def __init__(self, max_age):
        self.alive = True
        self.age = 0
        self.location = None
        self.next = [None, None]
        self.name = None
        self.hasFood = False
        self.maxAge = max_age
        self.moved = False

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

    def unmove(self):
        self.moved = False

    def move(self, ants, foods, field):
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
            return 1 - dist/sqrt((field.size[0]*field.size[1])*2)

        def bell_weight(dist):
            max_smell_distance = 3
            min_smell_distance = 1
            if dist < max_smell_distance and dist > min_smell_distance:
                weight = (1-(dist/max_smell_distance)**2)**2
            else:
                weight = 0
            return weight

        def towards_food(self, food):
            vect = get_vector(self, food)
            dist = get_distance(get_vector(self, food))
            normed = normalize(vect, dist)
            weight = linear_weight(dist)
            influences.append((weight, normed))

        def towards_hive(self):
            pass

        def towards_ant(self, ant):
            vect = get_vector(self, ant)
            dist = get_distance(get_vector(self, ant))
            if dist == 0:
                return 0
            normed = normalize(vect, dist)
            weight = bell_weight(dist)
            influences.append((weight, normed))

        if self.alive is True:
            if self.hasFood is True:
                towards_hive(self)
            else:
                for food in foods:
                    if self.location == food.location:
                        self.die()
                        field.grid[self.getX(), self.getY()] = field.food
                        return
                    towards_food(self, food.location)

            for ant in ants:
                if ant.name == self.name:
                    continue
                else:
                    towards_ant(self, ant.location)

            x, y = final_direction()

            self.next = dc(self.location)
            if x >= 0.5:
                self.next[0] += 1
            elif x <= -0.5:
                self.next[0] -= 1
            if y >= 0.5:
                self.next[1] += 1
            elif y <= -0.5:
                self.next[1] -= 1
            self.getOlder()


def collision_check(ants, field):
    locked = []
    random_walker = []

    def lock_move(ant, location):
        field.grid[ant.getX(), ant.getY()] = field.free
        ant.location = location
        ant.moved = True
        field.grid[ant.getX(), ant.getY()] = field.ant
        locked.append(location)

    def trickle_down(ants, field):
        detect_movement = True
        while detect_movement is True:
            detect_movement = False
            for ant in ants:
                if (ant.moved is False and ant.next in locked):
                    if ant.location in locked:
                        print("aha")
                    detect_movement = True
                    lock_move(ant, ant.location)
                    random_walker.append(ant)

    def random_walk(ants, field):
        [ant.unmove() for ant in ants]

        def is_valid(number):
            if number < 0 or number >= field.size[0]:
                return False
            else:
                return True

        def check_if_free(x, y, liste):
            if [x, y] not in locked and (is_valid(x) and is_valid(y)):
                liste.append([x, y])

        again = True
        while again is True:
            ants = [ant for ant in ants if ant.moved == False]
            again = False
            for ant in ants:
                valid_loc = []
                up = ant.location[0] - 1
                down = ant.location[0] + 1
                left = ant.location[1] - 1
                right = ant.location[1] + 1

                check_if_free(ant.getX(), left, valid_loc)
                check_if_free(ant.getX(), right, valid_loc)
                check_if_free(up, left, valid_loc)
                check_if_free(down, left, valid_loc)
                check_if_free(up, right, valid_loc)
                check_if_free(down, right, valid_loc)
                check_if_free(up, ant.getY(), valid_loc)
                check_if_free(down, ant.getY(), valid_loc)

                if len(valid_loc) == 0:
                    again = True
                    continue

                lock_move(ant, valid_loc[rnd.randint(0, len(valid_loc)-1)])

    for ant in ants:
        if ant.location == ant.next:
            lock_move(ant, ant.location)
            random_walker.append(ant)

    trickle_down(ants, field)

    for ant in ants:
        if (ant.moved is False and ant.next not in locked):
            lock_move(ant, ant.next)

    trickle_down(ants, field)

    if len(random_walker) != 0:
        random_walk(random_walker, field)

    for x in range(0, len(locked)):
        lul = locked[x]
        if x != len(locked) -1:
            if lul in locked[x+1:len(locked)]:
                print("fuck")
    ants = [ant.unmove() for ant in ants]

def get_ant_names():
    url = """http://www.babynamewizard.com/baby-name/
             advanced-name-finder/results?start=Ant"""
    url = url.replace("\n", "").replace(" ", "")  # replace whitespaces
    try:
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

    except:
        print("no connection to the internet")
        names = ["{}".format(x) for x in range(0, 40)]
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
