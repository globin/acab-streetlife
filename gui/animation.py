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

    def SetFile(self, tmp):
        self.file = tmp

    def GetFile(self):
        return self.file

    def SetName(self, tmp):
        self.name = tmp

    def GetName(self):
        return self.name

    def SetConfig(self, tmp):
        self.config = tmp

    def GetConfig(self):
        return self.config

    def SetTime(self, tmp):
        self.time = tmp

    def GetTime(self):
        return self.time

    def SetColor(self, tmp):
        self.color = tmp

    def GetColor(self):
        return self.color

    def SetPreview(self, tmp):
        self.preview = tmp

    def GetPreview(self):
        return self.preview

    def GetParsedConfig(self):
        tmp = self.config[:]

        if self.color:
            for i,c in enumerate(tmp):
                print c
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
                    tmp.SetFile(os.path.join(path, line))
                    counter = counter + 1
                # Config
                elif counter == 1:
                    if line != "#":
                        config = line.split(",")
                        tmp.SetConfig(config)

                    counter = counter + 1
                # Name
                elif counter == 2:
                    tmp.SetName(line)
                    counter = counter + 1
                # Preview
                elif counter == 3:
                    if line != "#":
                        tmp.SetPreview(os.path.join(path, line))

                    animations_list.append(tmp)
                    counter = 0

            return animations_list
