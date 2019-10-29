# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:39:07 2019

@author: ElJocho
"""
from copy import deepcopy as dc
import random as rnd
import requests
import src.errors as err
import src.utils as utils


class Ant:
    """used to build and manage ant objects"""
    names = []
    nextName = [0]  # list, because they are mutable making them accessible from all instances

    def __init__(self, max_age: int = 100, age: int = 0):
        self.alive = True
        self.age = age
        self.location = None
        self.next = [None, None]
        self.name = None  # yes ants have names, it is not important for anything, except cuteness
        self.has_food = False
        self.max_age = max_age
        self.moved = False

    def get_older(self, field):
        """used to make ants only live to a maximum age set in settings.txt"""
        if self.age < self.max_age:
            self.age += 1
        else:
            self.die()
            field.set_cell(self.location, field.FREE)

    def die(self):
        """remove ant from simulation"""
        self.alive = False

    def get_x(self):
        """get variable x. This docstring was sponsored by pylint."""
        return self.location[0]

    def get_y(self):
        """get variable y. This docstring was sponsored by pylint."""
        return self.location[1]

    def set_name(self):
        """give ant a name"""
        try:
            self.name = self.names[self.nextName[0]]
            self.nextName[0] += 1
        except IndexError:
            self.name = self.generate_name()
            self.names.append(self.name)
            self.nextName[0] += 1

    def reset_moved(self):
        """reset ant.moved to false"""
        self.moved = False

    def generate_name(self):
        """randomly generate name starting with 'ant'"""
        double_entry = True
        while double_entry is True:
            vowels = "aeiuyo"
            consonants = "bcdfghjklmnpqrstvwxz"
            name = "Ant" + rnd.choice(vowels) + rnd.choice(consonants)
            if 2 / rnd.choice([1, 2]) == 1:  # in average every second name gets extra vowel
                name += rnd.choice(vowels)
            if name not in self.names:
                double_entry = False
        return name

    def move(self, ants, foods, hive, field):
        """set desired locations for ants"""
        influences = []

        def get_vector(goal):
            """generate vector"""
            rel_x = goal[0] - self.get_x()
            rel_y = goal[1] - self.get_y()
            return rel_x, rel_y

        def final_direction():
            """calculate final vector"""
            sum_weight = 0.
            weighted_x = 0.
            weighted_y = 0.
            for entry in influences:
                sum_weight += entry[0]
                weighted_x += entry[0] * entry[1][0]
                weighted_y += entry[0] * entry[1][1]
            if sum_weight == 0:
                new_x = new_y = 0
            else:
                new_x = weighted_x / sum_weight
                new_y = weighted_y / sum_weight

            return new_x, new_y

        def towards_goal(goal):
            """coordinate the steps to generate a vector towards a goal"""
            vect = get_vector(goal)
            dist = utils.get_distance(vect)
            normed = utils.normalize(vect, dist)
            weight = utils.linear_weight(dist, field)
            influences.append([weight, normed])

        def towards_ant(ant):
            """coordinate the stepts to generate a vector towards an ant"""
            vect = get_vector(ant)
            dist = utils.get_distance(get_vector(ant))
            if dist == 0:
                raise err.MovementError
            normed = utils.normalize(vect, dist)
            weight = utils.bell_weight(dist)
            influences.append([weight, normed])

        for food in foods:
            if self.location == food.location and self.has_food is False:
                self.has_food = True
                food.nom()

        if self.location == hive.location and self.has_food is True:
            hive.food += 1
            self.has_food = False

        if self.has_food is True:
            towards_goal(hive.location)
            influences[0][0] *= 2  # double the impact towards Hive
        else:
            for food in foods:
                towards_goal(food.location)

        for ant in ants:
            if ant is self:
                continue
            towards_ant(ant.location)

        new_x, new_y = final_direction()

        self.next = dc(self.location)
        if new_x >= 0.5:
            self.next[0] += 1
        elif new_x <= -0.5:
            self.next[0] -= 1
        if new_y >= 0.5:
            self.next[1] += 1
        elif new_y <= -0.5:
            self.next[1] -= 1
        self.get_older(field)

    @classmethod
    def get_ant_names(cls):
        """load all names from babynamewizard.com starting with 'ant'"""
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
            for line in lines:
                if line.find("girl/") != -1:
                    name = line[line.find("girl/") + 5:line.find("\" class")]
                elif line.find("boy/") != -1:
                    name = line[line.find("boy/") + 4:line.find("\" class")]
                else:
                    continue
                if len(name) >= 1:
                    cls.names.append(name)
            cls.names.append("antifa")
            cls.names.append("antman")

        except requests.ConnectionError:
            print("no connection to the internet")


class Food:
    """used to build and manage Food objects"""
    def __init__(self, location=None):
        self.amount = rnd.randint(4, 20)
        self.location = location

    def get_x(self):
        """get variable x. This docstring was sponsored by pylint."""
        return self.location[0]

    def get_y(self):
        """get variable y. This docstring was sponsored by pylint."""
        return self.location[1]

    def nom(self):
        """ant takes a bite"""
        self.amount -= 1

    def is_free(self, ants, field):
        """check if any ant is on top of a food object. If there is none, display food on grid"""
        free = True
        for ant in ants:
            if ant.location == self.location:
                free = False
        if free is True:
            field.set_cell(self.location, field.FOOD)


class Hive:
    """used to build and manage Hive objects"""
    def __init__(self, location):
        self.location = location
        self.food = 0
        self.cooldown = 0
        self.food_needed_to_spawn_ant = 3

    def spawn_ant(self, ants, field):
        """spawns a new ant, which consumes x food"""
        self.food -= self.food_needed_to_spawn_ant
        max_age = ants[0].max_age
        new_ant = Ant(max_age)
        new_ant.location = self.location
        new_ant.set_name()
        field.set_cell(new_ant.location, field.ANT)
        ants.append(new_ant)
        return ants

    def reset_cooldown(self):
        """resets the cooldown to 4 turns"""
        self.cooldown = 4

    def reduce_cooldown(self):
        """reduce cooldown by one to a minimum of 0"""
        if self.cooldown > 0:
            self.cooldown -= 1

    def is_ready(self):
        """reduce cooldown then check if ant can be """
        self.reduce_cooldown()
        if self.cooldown == 0 and self.food >= self.food_needed_to_spawn_ant:
            return True
        return False

    def get_x(self):
        """get variable x. This docstring was sponsored by pylint."""
        return self.location[0]

    def get_y(self):
        """get variable y. This docstring was sponsored by pylint."""
        return self.location[1]

    def is_free(self, ants, field):
        """check if any ant is on top of a hive object. If there is none, display food on grid"""
        free = True
        for ant in ants:
            if ant.location == self.location:
                free = False
        if free is True:
            field.set_cell(self.location, field.HIVE)
            return True
        return False
