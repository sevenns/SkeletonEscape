#!/usr/bin/env python
# coding=utf-8

import pygame
from pygame import *

# Необходимые константы
WINDOW_H = 640
WINDOW_W = 800
DISPLAY = (WINDOW_W, WINDOW_H)
BG_COLOR = "#000000"


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)  # Создание окна
    pygame.display.set_caption("Skeleton Escape")  # Заголовок окна
    bg = Surface(DISPLAY)  # Создание видимой поверхности
    bg.fill(Color(BG_COLOR))  # Заливка фона

    # Основной цикл
    while 1:
        for e in pygame.event.get():  # Обработка событий
            if e.type == QUIT:
                raise SystemExit
        screen.blit(bg, (0, 0))  # Перерисовка всего каждую итерацию цикла
        pygame.display.update()  # Обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
