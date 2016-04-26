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

items = [
    "textures/items/apple_golden.png"
]

grass = [
    "textures/blocks/crops_0.png",
    "textures/blocks/crops_1.png",
    "textures/blocks/crops_2.png",
    "textures/blocks/crops_3.png",
    "textures/blocks/crops_4.png",
    "textures/blocks/deadbush.png",
    "textures/blocks/flower.png",
    "textures/blocks/mushroom_brown.png",
    "textures/blocks/netherStalk_0.png",
    "textures/blocks/netherStalk_1.png",
    "textures/blocks/potatoes_0.png",
    "textures/blocks/rose.png",
    "textures/blocks/sapling.png",
    "textures/blocks/sapling_birch.png",
    "textures/blocks/sapling_jungle.png",
    "textures/blocks/sapling_spruce.png",
    "textures/blocks/stem_bent.png",
    "textures/blocks/stem_straight.png"
]


class Platform(sprite.Sprite):
    type = ""

    def __init__(self, x, y, type):
        sprite.Sprite.__init__(self)
        if type == "rock":
            self.image = image.load_extended(blocks[random.randint(1, 5)])
            self.type = "rock"
        elif type == "dirt":
            self.image = image.load_extended(blocks[0])
            self.type = "dirt"
        elif type == "apple":
            self.image = image.load_extended(items[0])
            self.type = "apple"
        elif type == "grass":
            self.image = image.load_extended(grass[random.randint(0, 17)])
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def destroy(self):
        pass

    def get_type(self):
        return self.type
