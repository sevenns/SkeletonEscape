#!/usr/bin/env python
# coding=utf-8

import pygame
from Camera import *
from Player import *
from pygame import *
from Platform import *
from Launcher import WINDOW_WIDTH
from Launcher import WINDOW_HEIGHT


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


def draw_level(level, entities, platforms, breakable, illusionary):
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
                pf = Platform(x, y, "bone")
                entities.add(pf)
                breakable.append(pf)
            elif col == ";":
                pf = Platform(x, y, "grass")
                entities.add(pf)
                illusionary.append(pf)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0


def start_game(screen, bg):
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
    draw_level(level, entities, platforms, breakable, illusionary)
    timer = pygame.time.Clock()  # Ограничитель FPS

    # Создаем объект камеры
    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # Высчитываем фактическую высоту уровня
    camera = Camera(camera_configure, total_level_width, total_level_height)

    # Основной цикл
    while True:
        if skeleton.died:
            draw_level(level, entities, platforms, breakable, illusionary)
            skeleton.died = False
            skeleton.bones = 0

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

        # Очки игрока
        bones_msg = "Bones: " + str(skeleton.bones)
        font_obj = pygame.font.SysFont("Harrington", 32)
        text_surface = font_obj.render(bones_msg, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (100, 25)
        screen.blit(text_surface, text_rect)

        # Отрисовываем каждую итерацию объекты(необходимо для правильной работы камеры)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()  # Обновление всего окна игры
