#!/usr/bin/env python
# coding=utf-8

import os
from pygame import *
from Intro import *
from Game import *


class Launcher(object):
    __window_width = 800
    __window_height = 640

    def main_start(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Центрирование окна при запуске
        pygame.init()  # Инициализация py game
        screen = pygame.display.set_mode((self.__window_width, self.__window_height))  # Создание окна
        pygame.display.set_caption("Skeleton Escape Alpha 0.1")  # Заголовок окна
        bg = Surface((self.__window_width, self.__window_height))  # Создание видимой поверхности фона
        bg_img = image.load_extended("textures/backgrounds/night.png")  # Подгрузка фона
        bg.blit(bg_img, (0, 0))  # Отрисовка фона

        # Основные функции игры
        game_intro = Intro()
        game_intro.start_intro(screen, bg)  # Сначала показываем меню
        game_start = Game()
        game_start.start_game(screen, bg)

    @staticmethod
    def get_window_width():
        return Launcher.__window_width

    @staticmethod
    def get_window_height():
        return Launcher.__window_height

# Создаем и запускаем новую игру
if __name__ == "__main__":
    game = Launcher()
    game.main_start()
