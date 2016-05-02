#!/usr/bin/env python
# coding=utf-8

import pygame
from pygame import *


class Intro(object):
    __intro_music = "sounds/intro.wav"
    _sound = True

    def start_intro(self, screen, bg):
        intro = True
        bg_img = image.load_extended("textures/backgrounds/night.png")  # Подгрузка фона
        bg.blit(bg_img, (0, 0))  # Отрисовка фона
        pygame.mixer.music.load(self.__intro_music)
        pygame.mixer.music.play(-1)

        font_obj = pygame.font.SysFont("Harrington", 32)
        play_color = [210, 215, 211]
        sound_color = [210, 215, 211]
        if Intro.check_sound():
            check_sound = "ON"
        else:
            check_sound = "OFF"
        exit_color = [210, 215, 211]
        while intro:
            screen.blit(bg, (0, 0))  # Отрисовка фона

            play_surface = font_obj.render("PLAY", True, play_color)  # Создаем поверхность с текстом
            play_rect = play_surface.get_rect()  # Получаем область поверхности с текстом
            play_rect.center = (650, 300)  # Задаем координаты этой области
            screen.blit(play_surface, play_rect)  # Выводим текст
            sound_surface = font_obj.render("Music: " + check_sound, True, sound_color)
            sound_rect = sound_surface.get_rect()
            sound_rect.center = (650, 350)
            screen.blit(sound_surface, sound_rect)
            exit_surface = font_obj.render("Exit", True, exit_color)
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

    @staticmethod
    def check_sound():
        return Intro._sound
