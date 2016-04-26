#!/usr/bin/env python
# coding=utf-8

import pygame
import pyganim
from Camera import *
from Player import *
from Blocks import *
from pygame import *

# Необходимые константы
WINDOW_H = 640
WINDOW_W = 800
DISPLAY = (WINDOW_W, WINDOW_H)
BG_COLOR = "#FFFFFF"


# Конфигурация камеры
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WINDOW_W / 2, -t + WINDOW_H / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WINDOW_W), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WINDOW_H), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)  # Создание окна
    pygame.display.set_caption("Skeleton Escape")  # Заголовок окна
    bg = Surface(DISPLAY)  # Создание видимой поверхности
    bg.fill(Color(BG_COLOR))  # Заливка фона

    # Создание объекта Player
    player = Player(55, 55)
    left = right = False  # Обездвиживаем игрока
    up = False

    # Ищем entity
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # То, что может служить опорой или барьером
    entities.add(player)

    # Уровень
    level = [
        "                                            ",
        "                                            ",
        "                                            ",
        "                                            ",
        "             __                             ",
        "                                            ",
        "__                                          ",
        "                                            ",
        "                    ___                     ",
        "                  ######                    ",
        "                                            ",
        "      ___                                   ",
        "                                            ",
        "   ___________                              ",
        "   __########__                             ",
        "                 _                          ",
        "                    __                      ",
        "     _____                                  ",
        "   ___###__________                         ",
        "###########################_________________"
    ]
    timer = pygame.time.Clock()  # Ограничитель FPS

    x = y = 0
    for row in level:
        for col in row:
            if col == "_":
                # Создание и заливка блока
                pf = Platform(x, y, "rock")
                entities.add(pf)
                platforms.append(pf)
            elif col == "#":
                # Создание и заливка блока
                pf = Platform(x, y, "dirt")
                entities.add(pf)
                platforms.append(pf)
            x += WIDTH
        y += HEIGHT
        x = 0

    # Создаем объект камеры
    total_level_width = len(level[0])*WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*HEIGHT # высоту
    camera = Camera(camera_configure, total_level_width, total_level_height)

    # Основной цикл
    while 1:
        timer.tick(60)
        for e in pygame.event.get():  # Обработка событий
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == QUIT:
                raise SystemExit
        screen.blit(bg, (0, 0))  # Перерисовка всего каждую итерацию цикла

        player.update(left, right, up, platforms)
        camera.update(player)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()  # Обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
