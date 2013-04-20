#!/usr/bin/env python

import os

class Animation:
    def __init__(self):
        self.file = ""
        self.name = ""

    def SetFile(self, tmp):
        self.file = tmp

    def GetFile(self):
        return self.file

    def SetName(self, tmp):
        self.name = tmp

    def GetName(self):
        return self.name

    def GetTime(self):
        return 10

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

                if counter == 0:
                    tmp = Animation()
                    tmp.SetFile(os.path.join(path, line))
                    counter = counter + 1
                elif counter == 1:
                    tmp.SetName(line)
                    animations_list.append(tmp)
                    counter = 0

            return animations_list
