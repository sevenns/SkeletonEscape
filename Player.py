#!/usr/bin/env python
# coding=utf-8

import Game
import pyganim
import pygame
from pygame import *


class Player(pygame.sprite.Sprite):
    __width = 26  # Ширина игрока
    __height = 41  # Высота игрока
    __jump_power = 8  # Сила прыжка игрока
    __gravity = 0.45  # Гравитация
    __color = "#AA3311"  # Цвет
    __animation_delay = 0.14  # Длительность одного кадра при анимации
    __animation_run = [  # Анимация бега
        "textures/skelet/walk-1.png",
        "textures/skelet/walk-2.png",
        "textures/skelet/walk-3.png",
        "textures/skelet/walk-4.png"
    ]
    __animation_stay = [("textures/skelet/idle.png", 0.1)]  # Анимация неподвижности
    __die_sound = "sounds/skeleton/die.wav"

    # Инициализация
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.bones = 0  # Кол-во костей у игрока
        self.score = 0  # Очки игрока
        self.died = False  # Умер ли игрок
        self.jump_power = 0  # Скорость по y
        self.on_ground = False  # Стоит ли игрок на земле
        self.start_position_x = x  # Начальная позиция по x
        self.start_position_y = y  # Начальная позиция по y
        self.image = Surface((self.__width, self.__height))
        self.image.fill(Color(self.__color))
        self.rect = Rect(x, y, self.__width, self.__height)

        # Необходимое для анимации персонажа
        self.image.set_colorkey(Color(self.__color))  # Прозрачный фон
        # Анимация ходьбы
        animations = []
        for animation in self.__animation_run:
            animations.append((animation, self.__animation_delay))
        self.animation_run = pyganim.PygAnimation(animations)
        self.animation_run.play()
        # Анимация в простое
        self.animation_stay = pyganim.PygAnimation(self.__animation_stay)
        self.animation_stay.play()
        self.animation_stay.blit(self.image, (0, 0))

    # Отрисовка игрока
    def update(self, player_jump, game_difficult, platforms, illusionary, breakable):
        if player_jump:
            if self.on_ground:
                self.jump_power = -self.__jump_power
                self.image.fill(Color(self.__color))
                self.animation_stay.blit(self.image, (0, 0))
        if not player_jump and self.jump_power == 0:
            self.image.fill(Color(self.__color))
            self.animation_run.blit(self.image, (0, 0))  # Проигрываем анимацию движения
        if not self.on_ground:
            self.jump_power += self.__gravity
        if self.rect.x < self.start_position_x:
            self.rect.x += 1

        self.on_ground = False
        self.rect.y += self.jump_power  # Перенос позицию игрока по y
        self.collide(self.jump_power, game_difficult, platforms, illusionary, breakable)

    # Столькновения с объектами
    def collide(self, y_speed, game_difficult, platforms, illusionary, breakable):
        for p in platforms:
            if sprite.collide_rect(self, p):  # Если есть пересечение платформы с игроком
                # Обездвиживаем при падении вниз
                if y_speed > 0:
                    if p.rect.y + p.rect.bottom > self.rect.centery > p.rect.y:
                        self.rect.x -= game_difficult * 2
                    else:
                        self.rect.bottom = p.rect.top
                        self.on_ground = True
                        self.jump_power = 0
                # Обездвиживаем при прыжке
                if y_speed < 0 and self.rect.top >= p.rect.bottom - 5:
                    self.rect.top = p.rect.bottom
                    self.jump_power = 0
        for i in illusionary:
            if sprite.collide_rect(self, i):
                pass
        for b in breakable:
            if sprite.collide_rect(self, b) and b.get_exist():
                self.bones += 1
                self.score += 150
                b.destroy()

    def die(self):
        pygame.mixer.Sound(self.__die_sound).play(0, 0, 0)
        time.wait(2000)
        self.died = True
        self.bones = 0
        self.score = 0
        self.rect.x = self.start_position_x
        self.rect.y = self.start_position_y

    def get_player_width(self):
        return self.__width

    def get_player_height(self):
        return self.__height
