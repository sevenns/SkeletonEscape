#!/usr/bin/env python
# coding=utf-8

import pygame
from pygame import *


class Intro(object):
    __intro_music = "sounds/intro.wav"

    def start_intro(self, screen, bg):
        intro = True
        pygame.mixer.music.load(self.__intro_music)
        pygame.mixer.music.play()
        while intro:
            screen.blit(bg, (0, 0))
            for e in pygame.event.get():
                if e.type == QUIT:
                    raise SystemExit
                if e.type == KEYDOWN and e.key == K_KP_ENTER:
                    intro = False
                    pygame.mixer.music.stop()
            font_obj = pygame.font.SysFont("Harrington", 32)
            text_surface = font_obj.render("Press ENTER for play", True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.center = (600, 380)
            screen.blit(text_surface, text_rect)
            pygame.time.Clock().tick(15)
            pygame.display.update()