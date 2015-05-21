#!/usr/bin/env python

import os

class Animation:
    def __init__(self):
        self.file = ""
        self.name = ""
        self.config = []
        self.time = 60
        self.color=None
        self.preview=None
        self.fadetime="0"

    @property
    def parsedConfig(self):
        tmp = self.config[:]

        if self.color:
            for i,c in enumerate(tmp):
                if c == "%r":
                    tmp[i] = str(self.color[0])
                elif c == "%g":
                    tmp[i] = str(self.color[1])
                elif c == "%b":
                    tmp[i] = str(self.color[2])

        return tmp

    @staticmethod
    def LoadFromFile(filename):
        animations_list = []

        path = os.path.dirname(os.path.abspath(filename))

        with open(filename) as f:
            content = f.readlines()

            tmp = None
            counter = 0
            for line in content:
                line = line[0:-1] # Crop newline

                if line == "":
                    counter = 0
                    continue

                # File
                if counter == 0:
                    tmp = Animation()
                    tmp.file = os.path.join(path, line)
                    counter += 1
                # Config
                elif counter == 1:
                    if line != "#":
                        config = line.split(",")
                        tmp.config = config

                    counter += 1
                # Name
                elif counter == 2:
                    tmp.name = line
                    counter += 1
                # Preview
                elif counter == 3:
                    if line != "#":
                        tmp.preview = os.path.join(path, line)

                    counter += 1
                # FadeTime
                elif counter == 4:
                    if line != "#":
                        tmp.fadetime = line #TODO int or float?

                    animations_list.append(tmp)
                    counter = 0

            return animations_list
