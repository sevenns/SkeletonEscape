#!/usr/bin/env python
# coding=utf-8

import py2exe.py2exe_util
import os
import pygame
from pygame import *
from Intro import Intro
from Game import Game


class Launcher(object):
    __window_width = 800  # Ширина окна
    __window_height = 640  # Высота окна
    __window_icon = image.load_extended("textures/items/bone.png")  # Иконка

    def main_start(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Центрирование окна при запуске
        pygame.init()  # Инициализация py game
        screen = pygame.display.set_mode((self.__window_width, self.__window_height))  # Создание окна
        pygame.display.set_icon(self.__window_icon)
        pygame.display.set_caption("Skeleton Escape Alpha 0.1")  # Заголовок окна
        bg = Surface((self.__window_width, self.__window_height))  # Создание видимой поверхности фона
        exit_flag = False
        game_intro = Intro()
        game_start = Game()

        # Основные функции игры
        while not exit_flag:
            if game_intro.start_intro(screen, bg):  # Сначала показываем меню
                exit_flag = True
            else:
                game_start.start_game(screen, bg, self.__window_width, self.__window_height)  # Запуск игры

# Создаем и запускаем новую игру
if __name__ == "__main__":
    game = Launcher()
    game.main_start()
