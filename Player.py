#!/usr/bin/env python
# coding=utf-8

import pygame
import pyganim
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

# Анимация в неподвижности
ANIMATION_STAY = [("textures/skelet/idle.png", 0.1)]

# Подгрузка звуков
DIE_SOUND = "sounds/skeleton/die.wav"
FOOTSTEP_SOUND = "sounds/skeleton/footstep.ogg"


class Player(sprite.Sprite):
    # Инициализация
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.bones = 0  # Кол-во костей у игрока
        self.score = 0  # Очки игрока
        self.died = False  # Умер ли игрок
        self.jump_power = 0  # Скорость по y
        self.move_speed = 0  # Скорость по x
        self.on_ground = False  # Стоит ли игрок на земле
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
        self.walk_animation = pyganim.PygAnimation(animations)
        self.walk_animation.play()
        # Анимация в простое
        self.stay_animation = pyganim.PygAnimation(ANIMATION_STAY)
        self.stay_animation.play()
        self.stay_animation.blit(self.image, (0, 0))

    # Обновление изменений
    def update(self, up, platforms, illusionary, breakable):
        if up:
            if self.on_ground:
                self.jump_power = -JUMP
                self.image.fill(Color(COLOR))
                self.stay_animation.blit(self.image, (0, 0))
        if not up and self.jump_power == 0:
            # Проигрываем анимацию движения
            self.image.fill(Color(COLOR))
            self.walk_animation.blit(self.image, (0, 0))
            # Проигрываем звуки шагов
            # pygame.mixer.Sound(FOOTSTEP_SOUND).play(0, 0, 1)
        if not self.on_ground:
            self.jump_power += GRAVITY

        if self.rect.y > MIN_HEIGHT:
            self.die()
        self.on_ground = False
        self.rect.y += self.jump_power  # Перенос позицию игрока по y
        self.rect.x += self.move_speed
        self.collide(self.move_speed, self.jump_power, platforms, illusionary, breakable)

    def collide(self, x_speed, y_speed, platforms, illusionary, breakable):
        for p in platforms:
            if sprite.collide_rect(self, p):  # Если есть пересечение платформы с игроком
                # Обездвиживаем при падении вниз
                if y_speed > 0:
                    if self.rect.y == p.rect.y - 9:
                        self.rect.right = p.rect.left
                    else:
                        self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.jump_power = 0
                # Обездвиживаем при прыжке
                if y_speed < 0:
                    self.rect.top = p.rect.bottom
                    self.jump_power = 0
        for i in illusionary:
            if sprite.collide_rect(self, i):
                pass
        for b in breakable:
            if sprite.collide_rect(self, b) and b.exist:
                self.bones += 1
                self.score += 500
                b.destroy()

    def die(self):
        pygame.mixer.Sound(DIE_SOUND).play(0, 0, 0)
        time.wait(2000)
        self.died = True
        self.stopped = False
        self.bones = 0
        self.score = 0
        self.rect.x = self.start_x
        self.rect.y = self.start_y
