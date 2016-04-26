#!/usr/bin/env python
# coding=utf-8

from pygame import *

WIDTH = 22
HEIGHT = 32
MOVE_SPEED = 7
JUMP = 7
GRAVITY = 0.35
COLOR = "#AA3311"


class Player(sprite.Sprite):
    # Инициализация
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.x_speed = 0 # Скорость по x
        self.y_speed = 0 # Скорость по y
        self.isStay = False # Стоит ли игрок на земле или нет
        self.start_x = x # Начальная позиция по x
        self.start_y = y # Начальная позиция по y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    # Обновление изменений
    def update(self, left, right, up):
        if up:
            if self.isStay:
                self.y_speed = -JUMP
        if left:
            self.x_speed = -MOVE_SPEED # Движение влево
        if right:
            self.x_speed = MOVE_SPEED # Движение вправо
        if not(left or right):
            self.x_speed = 0 # На месте
        if not self.isStay:
            self.y_speed += GRAVITY
        self.isStay = False
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed; # Перенос позицию игрока по x

    # Вывод всех изменений
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))