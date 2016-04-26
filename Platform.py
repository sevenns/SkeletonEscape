#!/usr/bin/env python
# coding=utf-8

from pygame import *
import random

# Необходимые константы
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

# Массив текстур
blocks = [
    "textures/blocks/gravel.png",
    "textures/blocks/stone.png",
    "textures/blocks/stonebrick.png",
    "textures/blocks/stoneMoss.png",
    "textures/blocks/brick.png",
    "textures/blocks/wood.png"
]


class Platform(sprite.Sprite):
    def __init__(self, x, y, type):
        sprite.Sprite.__init__(self)
        if type == "rock":
            self.image = image.load_extended(blocks[random.randint(1, 5)])
        elif type == "dirt":
            self.image = image.load_extended(blocks[0])
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
