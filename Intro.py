#!/usr/bin/env python
# coding=utf-8

import struct
import pygame
from pygame import *


class Intro(object):
    __intro_music = "sounds/intro.wav"
    _sound = True

    def __init__(self):
        self.__best_score = 0  # Лучший результат игрока

    def start_intro(self, screen, bg):
        intro = True
        bg_img = image.load_extended("textures/backgrounds/night.png")  # Подгрузка фона
        bg.blit(bg_img, (0, 0))  # Отрисовка фона
        self.__load_data("data", ".dat")  # Подгрузка данных
        pygame.mixer.music.load(self.__intro_music)  # Подгрузка музыки
        if Intro.check_sound():
            pygame.mixer.music.play(-1)  # Проигрывание музыки бесконечно

        best_font = pygame.font.SysFont("Harrington", 36)  # Шрифт рекорда
        menu_font = pygame.font.SysFont("Harrington", 32)  # Шрифт меню
        play_color = [210, 215, 211]
        sound_color = [210, 215, 211]

        if Intro.check_sound():
            check_sound = "ON"
        else:
            check_sound = "OFF"
        exit_color = [210, 215, 211]
        while intro:
            screen.blit(bg, (0, 0))  # Отрисовка фона

            # Вывод рекорда
            if self.__best_score != 0:
                best_surface = best_font.render("Best: " + str(self.__best_score), True, (255, 255, 255))
            else:
                best_surface = best_font.render("No have BEST", True, (255, 255, 255))
            best_rect = best_surface.get_rect()  # Получаем область поверхности
            best_rect.x, best_rect.y = 20, 20  # Задаем координаты отображения рекорда
            screen.blit(best_surface, best_rect)  # Отображаем текст

            play_surface = menu_font.render("PLAY", True, play_color)  # Создаем поверхность с текстом
            play_rect = play_surface.get_rect()  # Получаем область поверхности с текстом
            play_rect.center = (650, 300)  # Задаем координаты этой области
            screen.blit(play_surface, play_rect)  # Выводим текст
            sound_surface = menu_font.render("Music: " + check_sound, True, sound_color)
            sound_rect = sound_surface.get_rect()
            sound_rect.center = (650, 350)
            screen.blit(sound_surface, sound_rect)
            exit_surface = menu_font.render("Exit", True, exit_color)
            exit_rect = exit_surface.get_rect()
            exit_rect.center = (650, 400)
            screen.blit(exit_surface, exit_rect)
            for e in pygame.event.get():
                if e.type == KEYDOWN and e.key == K_RETURN:
                    intro = False
                    pygame.mixer.music.stop()
                if e.type == MOUSEBUTTONUP:
                    pos = mouse.get_pos()
                    if play_rect.collidepoint(pos):
                        intro = False
                        pygame.mixer.music.stop()
                    if sound_rect.collidepoint(pos):
                        if Intro._sound:
                            Intro._sound = False
                            check_sound = "OFF"
                            pygame.mixer.music.stop()
                        else:
                            Intro._sound = True
                            check_sound = "ON"
                            pygame.mixer.music.play(-1)
                    if exit_rect.collidepoint(pos):
                        return True
                if e.type == MOUSEMOTION:
                    pos = mouse.get_pos()
                    if play_rect.collidepoint(pos):
                        play_color = [255, 255, 255]
                    else:
                        play_color = [210, 215, 211]
                    if sound_rect.collidepoint(pos):
                        sound_color = [255, 255, 255]
                    else:
                        sound_color = [210, 215, 211]
                    if exit_rect.collidepoint(pos):
                        exit_color = [255, 255, 255]
                    else:
                        exit_color = [210, 215, 211]
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    return True
                if e.type == QUIT:
                    raise SystemExit
            pygame.time.Clock().tick(60)
            pygame.display.update()

    def __save_data(self, file_name, file_ext):
        write_file = open(file_name + file_ext, "wb")
        score_for_saving = struct.pack(">i", self.__best_score)
        write_file.write(score_for_saving)
        write_file.close()

    def __load_data(self, file_name, file_ext):
        try:
            load_file = open(file_name + file_ext, "rb")
        except (OSError, IOError):
            load_file = open(file_name + file_ext, "wb")
            load_file.write(struct.pack(">i", 0))
            load_file.close()
            load_file = open(file_name + file_ext, "rb")
        score_for_saving = load_file.read()
        self.__best_score = struct.unpack(">i", score_for_saving)[0]
        load_file.close()

    @staticmethod
    def check_sound():
        return Intro._sound
