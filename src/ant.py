# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:39:07 2019

@author: ElJocho
"""
import requests


class ant():
    def __init__(self):
        self.alive = True
        self.age = 0
        self.location = None
        self.name = None

    def move(self):
        if self.alive is True:
            self.getOlder()

    def getOlder(self):
        if self.age < 79:
            self.age += 1
        else:
            self.die()

    def die(self):
        self.alive = False


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
