#!/usr/bin/env python
# coding=utf-8

import pygame
from Player import *
from pygame import *

# Необходимые константы
WINDOW_H = 640
WINDOW_W = 800
PLATFORM_H = 32
PLATFORM_W = 32
DISPLAY = (WINDOW_W, WINDOW_H)
BG_COLOR = "#FFFFFF"
PF_COLOR = "#333333"


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)  # Создание окна
    pygame.display.set_caption("Skeleton Escape")  # Заголовок окна
    bg = Surface(DISPLAY)  # Создание видимой поверхности
    bg.fill(Color(BG_COLOR))  # Заливка фона
    player = Player(55, 55) # создание объекта Player
    left = right = False # Обездвиживаем игрока
    up = False
    level = [
        "-------------------------",
        "-                       -",
        "-                       -",
        "-                       -",
        "-            --         -",
        "-                       -",
        "--                      -",
        "-                       -",
        "-                   --- -",
        "-                       -",
        "-                       -",
        "-      ---              -",
        "-                       -",
        "-   -----------         -",
        "-                       -",
        "-                -      -",
        "-                   --  -",
        "-                       -",
        "-                       -",
        "-------------------------"
    ]
    timer = pygame.time.Clock() # Ограничитель FPS

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

        x = y = 0
        for row in level:
            for col in row:
                if col == "-":
                    # Создание и заливка блока
                    pf = Surface((PLATFORM_W, PLATFORM_H))
                    pf.fill(Color(PF_COLOR))
                    screen.blit(pf, (x, y))
                x += PLATFORM_W
            y += PLATFORM_H
            x = 0

        player.update(left, right, up)
        player.draw(screen)
        pygame.display.update()  # Обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
