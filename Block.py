#!/usr/bin/env python
# coding=utf-8

import random
import pygame
from pygame import *


class Block(pygame.sprite.Sprite):
    __width = 32
    __height = 32

    def __init__(self, x, y, block_type):
        pygame.sprite.Sprite.__init__(self)
        self.__type = block_type  # Тип блока
        self.__exist = True  # Существование блока в мире
        self.__bone_texture = "textures/items/bone.png"  # Текстура кости
        self.__dirt_texture = "textures/blocks/dirt.png"  # Текстура грязи
        self.__grass_side_texture = "textures/blocks/grass_side.png"  # Текстура грязи с травой
        self.__grass_textures = [  # Текстуры травы
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
        self.__draw_block(x, y)

    def __draw_block(self, x, y):
        if self.__type == "dirt":
            self.image = image.load_extended(self.__dirt_texture)
        elif self.__type == "grass_side":
            self.image = image.load_extended(self.__grass_side_texture)
        elif self.__type == "bone":
            self.image = image.load_extended(self.__bone_texture)
        elif self.__type == "grass":
            self.image = image.load_extended(self.__grass_textures[random.randint(0, 12)])
        self.rect = Rect(x, y, self.__width, self.__height)

    def update(self, update_speed):
        self.rect.x -= update_speed  # Перенос позицию игрока по x

    def destroy(self):
        self.__exist = False
        self.kill()

    def get_type(self):
        return self.__type

    def get_exist(self):
        return self.__exist

    def set_exist(self, flag):
        self.__exist = flag

    @staticmethod
    def get_blocks_width():
        return Block.__width

    @staticmethod
    def get_blocks_height():
        return Block.__height
