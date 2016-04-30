#!/usr/bin/env python
# coding=utf-8

import random
import pygame
from pygame import *


class Block(pygame.sprite.Sprite):
    __width = 32
    __height = 32
    __block_textures = [  # Текстуры блоков
        "textures/blocks/gravel.png",
        "textures/blocks/stone.png",
        "textures/blocks/stonebrick.png",
        "textures/blocks/stoneMoss.png",
        "textures/blocks/brick.png",
        "textures/blocks/wood.png"
    ]
    __grass_textures = [  # Текстуры травы
        "textures/blocks/crops_3.png",
        "textures/blocks/crops_4.png",
        "textures/blocks/deadbush.png",
        "textures/blocks/flower.png",
        "textures/blocks/netherStalk_0.png",
        "textures/blocks/netherStalk_1.png",
        "textures/blocks/rose.png",
        "textures/blocks/sapling.png",
        "textures/blocks/sapling_birch.png",
        "textures/blocks/sapling_jungle.png",
        "textures/blocks/sapling_spruce.png",
        "textures/blocks/stem_bent.png",
        "textures/blocks/stem_straight.png"
    ]
    __bone_texture = "textures/items/bone.png"  # Текстура кости

    def __init__(self, x, y, block_type):
        pygame.sprite.Sprite.__init__(self)
        self.type = ""
        self.exist = True
        if block_type == "rock":
            self.image = image.load_extended(self.__block_textures[random.randint(0, 5)])
            self.type = "rock"
        elif block_type == "dirt":
            self.image = image.load_extended(self.__block_textures[0])
            self.type = "dirt"
        elif block_type == "bone":
            self.image = image.load_extended(self.__bone_texture)
            self.type = "bone"
        elif block_type == "grass":
            self.image = image.load_extended(self.__grass_textures[random.randint(0, 12)])
        self.rect = Rect(x, y, self.__width, self.__height)

    def update(self, update_speed):
        self.rect.x -= update_speed  # Перенос позицию игрока по x

    def destroy(self):
        self.exist = False
        self.kill()

    def get_type(self):
        return self.type

    @staticmethod
    def get_block_width():
        return Block.__width

    @staticmethod
    def get_block_height():
        return Block.__height
