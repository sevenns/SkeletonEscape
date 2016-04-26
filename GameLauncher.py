#!/usr/bin/env python
# coding=utf-8

import random
import pygame
import os
from Camera import *
from Player import *
from Platform import *
from pygame import *

# Необходимые константы
WINDOW_HEIGHT = 640
WINDOW_WIDTH = 800
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)


# Конфигурация камеры
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WINDOW_WIDTH / 2, -t + WINDOW_HEIGHT / 2
    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WINDOW_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WINDOW_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы
    return Rect(l, t, w, h)


# Основная функция
def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Центрирование окна при запуске
    pygame.init()  # Инициализация pygame
    screen = pygame.display.set_mode(WINDOW_SIZE)  # Создание окна
    pygame.display.set_caption("Skeleton Escape")  # Заголовок окна
    bg = Surface(WINDOW_SIZE)  # Создание видимой поверхности фона
    bg_img = image.load_extended("textures/backgrounds/night.png")  # Подгрузка самого фона
    bg.blit(bg_img, (0, 0))  # Отрисовка фона

    # Создание самого игрока
    skeleton = Player(55, 55)
    left = right = False  # Обездвиживаем игрока изначально
    up = False

    # Ищем entity
    entities = pygame.sprite.Group()  # Создаем группу для объектов
    platforms = []  # То, что может служить опорой или барьером
    illusionary = []  # То, через что можно пройти и оно не исчезнет
    breakable = []  # То, через что можно пройти и оно исчезнет
    entities.add(skeleton)  # Добавляем в объекты игрока

    # Уровень
    level = [
        "                                            ",
        "                                            ",
        "                                            ",
        "                                            ",
        "             __                             ",
        "                                            ",
        "__                                          ",
        "                    ;                       ",
        "                    ___                     ",
        "                  ######                    ",
        "                                            ",
        "      ___                                   ",
        "     ;;  ;                                  ",
        "   ___________                              ",
        "   __########__                             ",
        "                 _  ;                       ",
        "                    __                      ",
        "      ______   ;                            ",
        " ; ___###________     ;;    ;   ;;     @    ",
        "#################  ########___  ____ _______"
    ]
    timer = pygame.time.Clock()  # Ограничитель FPS

    # Отрисовка уровня по массиву level
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
            elif col == "@":
                pf = Platform(x, y, "apple")
                entities.add(pf)
                breakable.append(pf)
            elif col == ";":
                pf = Platform(x, y, "grass")
                entities.add(pf)
                illusionary.append(pf)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0

    # Создаем объект камеры
    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # Высчитываем фактическую высоту уровня
    camera = Camera(camera_configure, total_level_width, total_level_height)

    # Основной цикл
    while True:
        timer.tick(60)  # Выставляем ограничитель кадров в 60 FPS

        # Обработка событий
        for e in pygame.event.get():

            # Обрабатываем события нажатия клавиш для управления персонажем
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

            # Обрабатываем событие выхода
            if e.type == QUIT:
                raise SystemExit

        # Перерисовка персонажа
        skeleton.update(left, right, up, platforms, illusionary, breakable)
        # Перерисовка всего каждую итерацию цикла
        screen.blit(bg, (0, 0))
        # Обновление камеры по привязке к игроку
        camera.update(skeleton)

        # Отрисовываем каждую итерацию объекты(необходимо для правильной работы камеры)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        for i in illusionary:
            screen.blit(i.image, camera.apply(i))
        for b in breakable:
            screen.blit(b.image, camera.apply(b))
        pygame.display.update()  # Обновление всего окна игры

# Изначально запустить функцию main
if __name__ == "__main__":
    main()
