#!/usr/bin/env python
# coding=utf-8

import Platform
from pygame import *


class Bone(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load_extended("textures/items/bone.png")

    def collect(self):
        self.kill()
