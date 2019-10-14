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
import src.errors as err


class ant():
    def __init__(self, max_age, age=0):
        self.alive = True
        self.age = age
        self.location = None
        self.next = [None, None]
        self.name = None
        self.hasFood = False
        self.maxAge = max_age
        self.moved = False
        

    def getOlder(self, field):
        if self.age < self.maxAge:
            self.age += 1
        else:
            self.die(field)

    def die(self, field):
        self.alive = False
        field.grid[self.getX(), self.getY()] = field.free

    def getX(self):
        return self.location[0]

    def getY(self):
        return self.location[1]

    def unmove(self):
        self.moved = False

    def move(self, ants, foods, hive, field):
        influences = []

        def final_direction():
            sum_weight = 0.
            weighted_x = 0.
            weighted_y = 0.
            for entry in influences:
                sum_weight += entry[0]
                weighted_x += entry[0]*entry[1][0]
                weighted_y += entry[0]*entry[1][1]
            if sum_weight == 0:
                x = y = 0
            else:
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
            max_smell_distance = 2
            min_smell_distance = 1
            if dist < max_smell_distance and dist > min_smell_distance:
                weight = (1-(dist/max_smell_distance)**2)**2
            else:
                weight = 0
            return weight

        def towards_goal(self, food):
            vect = get_vector(self, food)
            dist = get_distance(get_vector(self, food))
            normed = normalize(vect, dist)
            weight = linear_weight(dist)
            influences.append((weight, normed))

        def towards_ant(self, ant):
            vect = get_vector(self, ant)
            dist = get_distance(get_vector(self, ant))
            if dist == 0:
                raise ValueError
            normed = normalize(vect, dist)
            weight = bell_weight(dist)
            influences.append((weight, normed))

        if self.alive is True:
            for food in foods:
                if self.location == food.location and self.hasFood is False:
                    self.hasFood = True
                    food.nom()

            if self.location == hive.location and self.hasFood is True:
                hive.food += 1
                self.hasFood = False

            if self.hasFood is True:
                towards_goal(self, hive.location)
                influences[0][0] * 2  # double the impact towards hive
            else:
                for food in foods:
                    towards_goal(self, food.location)

            for ant in ants:
                if ant is self:
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
            self.getOlder(field)


def collision_check(ants, field):
    locked = []

    def lock_move(ant, location):
        if location in locked:
            raise ValueError
        ant.location = location
        ant.moved = True
        locked.append(location)

    def trickle_down(ants, field):
        detect_movement = True
        while detect_movement is True:
            detect_movement = False
            for ant in ants:
                if (ant.moved is False and ant.next in locked):
                    detect_movement = True
                    random_walk(ant)

    def random_walk(ant):
        def is_valid(number):
            if number < 0 or number >= field.size[0]:
                return False
            else:
                return True

        def check_if_free(x, y, liste):
            if [x, y] not in locked and (is_valid(x) and is_valid(y)):
                liste.append([x, y])

        valid_loc = []
        up = ant.getX() - 1
        down = ant.getX() + 1
        left = ant.getY() - 1
        right = ant.getY() + 1

        check_if_free(ant.getX(), left, valid_loc)
        check_if_free(ant.getX(), right, valid_loc)
        check_if_free(up, left, valid_loc)
        check_if_free(down, left, valid_loc)
        check_if_free(up, right, valid_loc)
        check_if_free(down, right, valid_loc)
        check_if_free(up, ant.getY(), valid_loc)
        check_if_free(down, ant.getY(), valid_loc)

        if len(valid_loc) != 0:
            lock_move(ant, valid_loc[rnd.randint(0, len(valid_loc)-1)])
        elif ant.location not in locked:
            lock_move(ant, ant.location)
        else:
            raise err.MovementError

    for ant in ants:
        field.grid[ant.getX(), ant.getY()] = field.free
        if ant.location == ant.next and ant.moved is False:
            random_walk(ant)

    trickle_down(ants, field)

    for ant in ants:
        if (ant.moved is False and ant.next not in locked):
            lock_move(ant, ant.next)

    trickle_down(ants, field)

    for ant in ants:
        if ant.moved is False:
            print("Fuck!")

    for x in range(0, len(locked)):
        lul = locked[x]
        if x != len(locked) - 1:
            if lul in locked[x + 1:len(locked)]:
                print("fuck")

    [ant.unmove() for ant in ants]


class food():
    def __init__(self, location=None):
        self.amount = rnd.randint(4, 20)
        self.location = location

    def getX(self):
        return self.location[0]

    def getY(self):
        return self.location[1]

    def changeAmount(self, x):
        self.amount = self.amount + x

    def nom(self):
        self.amount -= 1

    def is_free(self, ants, field):
        free = True
        for ant in ants:
            if ant.location == self.location:
                free = False
        if free is True:
            field.grid[self.getX(), self.getY()] = field.food
            

class hive():
    def __init__(self, location):
        self.location = location
        self.food = 0
        self.cooldown = 0

    def spawn_ant(self, ants, field):
        maxAge = ants[0].maxAge
        new_ant = ant(maxAge)
        new_ant.location = self.location
        new_ant.name = gen_ant_name()
        ants.append(new_ant)
        return ants

    def reduce_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def is_ready(self):
        self.reduce_cooldown()
        if self.cooldown == 0 and self.food >= 5:
            return True

    def getX(self):
        return self.location[0]

    def getY(self):
        return self.location[1]

    def is_free(self, ants, field):
        free = True
        for ant in ants:
            if ant.location == self.location:
                free = False
        if free is True:
            field.grid[self.getX(), self.getY()] = field.hive
            return True


def gen_ant_name():
    vowels = "aeiuyo"
    consonants = "bcdfghjklmnpqrstvwxz"
    name = "ant" + rnd.choice(vowels) + rnd.choice(consonants)
    return name

def get_ant_names():
    url = """http://www.babynamewizard.com/baby-name/
             advanced-name-finder/results?start=Ant"""
    url = url.replace("\n", "").replace(" ", "")  # replace whitespaces
    try:
        data = requests.get(url)
        text = data.text
        # remove everything except lines with wanted content
        nametext = text[text.find("content-content"):
                        text.find("/content-content")]
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