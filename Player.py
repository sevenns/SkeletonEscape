#!/usr/bin/env python
# coding=utf-8

import random
import pyganim
import pygame
from pygame import *

# Необходимые константы
WIDTH = 26
HEIGHT = 41
MOVE_SPEED = 3
JUMP = 8
GRAVITY = 0.45
COLOR = "#AA3311"
MIN_HEIGHT = 896

# Константы анимаций
ANIMATION_DELAY = 0.14  # Длительность одного кадра
ANIMATION_DELAY_SUPER_SPEED = 0.05  # Длительность одного кадра при супер скорости

# Анимация ходьбы
ANIMATION_WALK = [
    "textures/skelet/walk-1.png",
    "textures/skelet/walk-2.png",
    "textures/skelet/walk-3.png",
    "textures/skelet/walk-4.png"
]

# Анимация неподвижности
ANIMATION_STAY = [("textures/skelet/idle.png", 0.1)]

# Подгрузка звуков
DIE_SOUND = "sounds/skeleton/die.wav"
FOOTSTEP_SOUND = "sounds/skeleton/footstep.ogg"


class Player(sprite.Sprite):
    # Инициализация
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.x_speed = 0  # Скорость по x
        self.y_speed = 0  # Скорость по y
        self.isStay = False  # Стоит ли игрок на земле или нет
        self.player_direction = False  # Направление взгляда
        self.start_x = x  # Начальная позиция по x
        self.start_y = y  # Начальная позиция по y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)

        # Необходимое для анимации персонажа
        self.image.set_colorkey(Color(COLOR))  # Прозрачный фон
        # Анимация ходьбы
        animations = []
        for animation in ANIMATION_WALK:
            animations.append((animation, ANIMATION_DELAY))
        self.walk_animation_right = pyganim.PygAnimation(animations)
        self.walk_animation_right.play()
        self.walk_animation_left = pyganim.PygAnimation(animations)
        self.walk_animation_left.flip(True, False)
        self.walk_animation_left.play()
        # Анимация в простое
        self.stay_animation = pyganim.PygAnimation(ANIMATION_STAY)
        self.stay_animation.play()
        self.stay_animation_reverse = pyganim.PygAnimation(ANIMATION_STAY)
        self.stay_animation_reverse.flip(True, False)
        self.stay_animation_reverse.play()
        self.stay_animation.blit(self.image, (0, 0))

    # Обновление изменений
    def update(self, left, right, up, platforms, illusionary, breakable):
        if up:
            if self.isStay:
                self.y_speed = -JUMP
            self.image.fill(Color(COLOR))
            if self.player_direction:
                self.stay_animation_reverse.blit(self.image, (0, 0))
            else:
                self.stay_animation.blit(self.image, (0, 0))
        if left:
            self.x_speed = -MOVE_SPEED  # Движение влево
            # Проигрываем анимацию движения
            self.image.fill(Color(COLOR))
            self.walk_animation_left.blit(self.image, (0, 0))
            # Проигрываем звуки ходьбы
            if not up and self.y_speed == 0:
                pygame.mixer.Sound(FOOTSTEP_SOUND).play(0, 0, 1)
            self.player_direction = True  # Меняем направление взгляда
        if right:
            self.x_speed = MOVE_SPEED  # Движение вправо
            # Проигрываем анимацию движения
            self.image.fill(Color(COLOR))
            self.walk_animation_right.blit(self.image, (0, 0))
            # Проигрываем звуки ходьбы
            if not up and self.y_speed == 0:
                pygame.mixer.Sound(FOOTSTEP_SOUND).play(0, 0, 1)
            self.player_direction = False  # Меняем направление взгляда
        if not(left or right):
            self.x_speed = 0  # На месте
        if not self.isStay:
            self.y_speed += GRAVITY
        if self.rect.y > MIN_HEIGHT:
            self.die()
        self.isStay = False
        self.rect.y += self.y_speed  # Перенос позицию игрока по y
        self.collide(0, self.y_speed, platforms, illusionary, breakable)
        self.rect.x += self.x_speed  # Перенос позицию игрока по x
        self.collide(self.x_speed, 0, platforms, illusionary, breakable)

    def collide(self, x_speed, y_speed, platforms, illusionary, breakable):
        for p in platforms:
            if sprite.collide_rect(self, p):  # Если есть пересечение платформы с игроком
                # Обездвиживаем, если движется вправо
                if x_speed > 0:
                    self.rect.right = p.rect.left
                # Обездвиживаем, если движется влево
                if x_speed < 0:
                    self.rect.left = p.rect.right
                # Обездвиживаем при падении вниз
                if y_speed > 0:
                    self.rect.bottom = p.rect.top
                    self.isStay = True
                    self.y_speed = 0
                # Обездвиживаем при прыжке
                if y_speed < 0:
                    self.rect.top = p.rect.bottom
                    self.y_speed = 0
        for i in illusionary:
            if sprite.collide_rect(self, i):
                pass
        for b in breakable:
            if sprite.collide_rect(self, b):
                b.destroy()

    def die(self):
        pygame.mixer.music.load(DIE_SOUND)
        pygame.mixer.music.play()
        time.wait(2000)
        self.rect.x = self.start_x
        self.rect.y = self.start_y
