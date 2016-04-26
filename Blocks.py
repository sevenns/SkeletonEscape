#!/usr/bin/env python
# coding=utf-8

from pygame import *

# Необходимые константы
HEIGHT = 32
WIDTH = 32
COLOR = "#333333"


class Platform(sprite.Sprite):
    def __init__(self, x, y, type):
        sprite.Sprite.__init__(self)
        if type == "rock":
            self.image = image.load("textures/blocks/x32/stone.png")
        elif type == "dirt":
            self.image = image.load("textures/blocks/x32/dirt.png")
        self.rect = Rect(x, y, WIDTH, HEIGHT)