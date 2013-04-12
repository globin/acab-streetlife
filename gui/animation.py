#!/usr/bin/env python

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

    @staticmethod
    def LoadFromFile(filename):
        animations_list = []

        with open(filename) as f:
            content = f.readlines()

            for line in content:
                tmp = Animation()
                tmp.SetFile(line[0:-1]) # Crop newline

                animations_list.append(tmp)

            return animations_list
