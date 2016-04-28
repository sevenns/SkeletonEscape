#!/usr/bin/env python
# coding=utf-8

import os
from pygame import *
from Intro import *
from Game import *

# Необходимые константы
WINDOW_HEIGHT = 640
WINDOW_WIDTH = 800


# Основная функция
def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Центрирование окна при запуске
    pygame.init()  # Инициализация pygame
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Создание окна
    pygame.display.set_caption("Skeleton Escape")  # Заголовок окна
    bg = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))  # Создание видимой поверхности фона
    bg_img = image.load_extended("textures/backgrounds/night.png")  # Подгрузка самого фона
    bg.blit(bg_img, (0, 0))  # Отрисовка фона

    # Основные функции игры
    game_intro(screen, bg)
    start_game(screen, bg)

# Изначально запустить функцию main
if __name__ == "__main__":
    main()
