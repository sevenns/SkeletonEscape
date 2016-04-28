#!/usr/bin/env python
# coding=utf-8

import pygame
from Zones import *
from Camera import *
from Player import *
from pygame import *
from Platform import *
from Launcher import WINDOW_WIDTH
from Launcher import WINDOW_HEIGHT

# Подгрузка звуков
GAME_MUSIC = "sounds/game.wav"


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


def clear_level(entities, platforms, to_delete_platforms, breakable, to_delete_breakable, illusionary, to_delete_illusionary):
    entities.remove(platforms)
    entities.remove(illusionary)
    entities.remove(breakable)
    for i in xrange(len(platforms)):
        platforms.__delitem__(0)
    for i in xrange(len(breakable)):
        breakable.__delitem__(0)
    for i in xrange(len(illusionary)):
        illusionary.__delitem__(0)
    for i in xrange(len(to_delete_platforms)):
        to_delete_platforms.__delitem__(0)
    for i in xrange(len(to_delete_breakable)):
        to_delete_breakable.__delitem__(0)
    for i in xrange(len(to_delete_illusionary)):
        to_delete_illusionary.__delitem__(0)


def draw_level(start_x, start_y, level, entities, platforms, breakable, illusionary):
    # Отрисовка уровня по массиву level
    x = start_x
    y = start_y
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
        x = start_x


def start_game(screen, bg):
    skeleton = Player(100, 100)  # Создание самого игрока
    up = False  # Изначально игрок не прыгает

    # Ищем entity
    entities = pygame.sprite.Group()  # Создаем группу для объектов
    platforms = []  # То, что может служить опорой или барьером
    to_delete_platforms = []  # Платформы, которые нужно будет удалить
    illusionary = []  # То, через что можно пройти и оно не исчезнет
    to_delete_illusionary = []
    breakable = []  # То, через что можно пройти и оно исчезнет
    to_delete_breakable = []
    entities.add(skeleton)  # Добавляем в объекты игрока

    draw_level(0, 0, start_zone, entities, platforms, breakable, illusionary)
    timer = pygame.time.Clock()  # Ограничитель FPS
    level_difficult = 3

    # Создаем объект камеры
    total_level_width = len(zones[random.randint(0, 1)][0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(zones[random.randint(0, 1)]) * PLATFORM_HEIGHT  # Высчитываем фактическую высоту уровня
    camera = Camera(camera_configure, total_level_width, total_level_height)

    # Проигрываем музыку
    pygame.mixer.Sound(GAME_MUSIC).play(-1, 0, 1)

    # Основной цикл
    while True:
        time_counter = timer.tick(60)  # Выставляем ограничитель кадров в 60 FPS

        if skeleton.died:
            clear_level(entities, platforms, to_delete_platforms, breakable, to_delete_breakable, illusionary, to_delete_illusionary)
            draw_level(0, 0, start_zone, entities, platforms, breakable, illusionary)
            entities.add(skeleton)  # Добавляем в объекты игрока
            skeleton.died = False
            level_difficult = 3
            time_counter = 0

        # Обработка событий
        for e in pygame.event.get():

            # Обрабатываем события нажатия клавиш для управления персонажем
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False

            # Обрабатываем событие выхода
            if e.type == QUIT:
                raise SystemExit

        if len(platforms) != 0 and platforms[len(platforms) - 1].rect.x < 1000:
            for p in platforms:
                to_delete_platforms.append(p)
            for i in illusionary:
                to_delete_illusionary.append(i)
            for b in breakable:
                to_delete_breakable.append(b)

            draw_level(skeleton.rect.x + 1000, 0, zones[random.randint(0, 2)], entities, platforms, breakable, illusionary)
        elif len(to_delete_platforms) != 0 and to_delete_platforms[len(to_delete_platforms) - 1].rect.x < -10:
            entities.remove(to_delete_platforms)
            entities.remove(to_delete_illusionary)
            entities.remove(to_delete_breakable)
            for i in xrange(len(to_delete_platforms)):
                platforms.__delitem__(0)
            for i in xrange(len(to_delete_illusionary)):
                illusionary.__delitem__(0)
            for i in xrange(len(to_delete_breakable)):
                breakable.__delitem__(0)
            to_delete_platforms = []
            to_delete_illusionary = []
            to_delete_breakable = []

        # Перерисовка персонажа
        skeleton.update(up, platforms, illusionary, breakable)
        for p in platforms:
            p.update(level_difficult)
        for i in illusionary:
            i.update(level_difficult)
        for b in breakable:
            b.update(level_difficult)
        # Перерисовка всего каждую итерацию цикла
        screen.blit(bg, (0, 0))
        # Обновление камеры по привязке к игроку
        camera.update(skeleton)

        # Кости игрока
        bones_msg = "Bones: " + str(skeleton.bones)
        font_obj = pygame.font.SysFont("Harrington", 32)
        text_surface = font_obj.render(bones_msg, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (100, 25)
        screen.blit(text_surface, text_rect)

        # Очки игрока
        skeleton.score += time_counter/10.0
        if skeleton.score > 3000:
            level_difficult = 4
        elif skeleton.score > 6000:
            level_difficult = 6
        score_msg = "Score: " + str(int(skeleton.score))
        font_obj = pygame.font.SysFont("Harrington", 32)
        text_surface = font_obj.render(score_msg, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (100, 60)
        screen.blit(text_surface, text_rect)

        # Отрисовываем каждую итерацию объекты(необходимо для правильной работы камеры)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()  # Обновление всего окна игры
