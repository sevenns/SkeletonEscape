#!/usr/bin/env python
# coding=utf-8

import pygame
from pygame import *
from Zones import *
from Camera import *
from Launcher import *
from Player import *
from Block import *


class Game(object):
    __game_music = "sounds/game.wav"
    __player = Player(100, 100)  # Создание самого игрока
    __level_difficult = 3  # Уровень сложности

    # Ищем entity
    __entities = pygame.sprite.Group()  # Создаем группу для объектов
    __platforms = []  # То, что может служить опорой или барьером
    __to_delete_platforms = []  # Платформы, которые нужно будет удалить
    __illusionary = []  # То, через что можно пройти и оно не исчезнет
    __to_delete_illusionary = []
    __breakable = []  # То, через что можно пройти и оно исчезнет
    __to_delete_breakable = []

    def start_game(self, screen, bg):
        self.__entities.add(self.__player)  # Добавляем в объекты игрока
        player_jump = False  # Изначально игрок не прыгает
        self.__draw_level(0, 0, start_zone)  # Отрисовываем уровень
        timer = pygame.time.Clock()  # Временной счетчик

        music = pygame.mixer.Sound(self.__game_music)  # Подгружаем музыку
        music.play(-1)  # Проигрываем музыку
        music.set_volume(0.3)  # Выставляем громкость музыке

        # Основной цикл
        while True:
            time_counter = timer.tick(60)  # Выставляем ограничитель кадров в 60 FPS

            # Действия после смерти игрока
            if self.__player.died:
                self.__clear_level()  # Очистка уровня для дальнейшей перерисовки
                self.__draw_level(0, 0, start_zone)  # Отрисовка уровня
                self.__entities.add(self.__player)  # Добавляем в объекты игрока
                self.__player.died = False  # Оживляем игрока
                self.__level_difficult = 3  # При каждом оживлении обнуляем уровень сложности
                time_counter = 0  # При каждом оживлении обнуляем временной счетчик

            # Создаем объект камеры
            total_level_width = len(start_zone[0]) * Block.get_block_width()  # Высчитываем фактическую ширину уровня
            total_level_height = len(start_zone) * Block.get_block_height()  # Высчитываем фактическую высоту уровня
            camera = Camera(self.camera_configure, total_level_width, total_level_height)

            # Обработка событий
            for e in pygame.event.get():
                if e.type == KEYDOWN and e.key == K_UP:  # Обработка события нажатия клавиши UP
                    player_jump = True
                if e.type == KEYUP and e.key == K_UP:  # Обработка события отпускания клавиши UP
                    player_jump = False
                if e.type == QUIT:  # Обрабатываем событие выхода из игры
                    raise SystemExit

            # Подгрузка уровня
            if len(self.__platforms) != 0 and self.__platforms[len(self.__platforms) - 1].rect.x < 1000:
                # Помечаем объекты, которые мы пробежали, как удаляемые
                for p in self.__platforms:
                    self.__to_delete_platforms.append(p)
                for i in self.__illusionary:
                    self.__to_delete_illusionary.append(i)
                for b in self.__breakable:
                    self.__to_delete_breakable.append(b)

                # Подгружаем к текущей зоне новую случайную
                self.__draw_level(self.__player.rect.x + 1000, 0, zones[random.randint(0, 3)])
            elif len(self.__to_delete_platforms) != 0 and self.__to_delete_platforms[len(self.__to_delete_platforms) - 1].rect.x < -10:
                # Удаляем объекты, которые игрок пробежал
                self.__entities.remove(self.__to_delete_platforms)
                self.__entities.remove(self.__to_delete_illusionary)
                self.__entities.remove(self.__to_delete_breakable)
                for i in xrange(len(self.__to_delete_platforms)):
                    self.__platforms.__delitem__(0)
                for i in xrange(len(self.__to_delete_illusionary)):
                    self.__illusionary.__delitem__(0)
                for i in xrange(len(self.__to_delete_breakable)):
                    self.__breakable.__delitem__(0)

                # Помечаем, что нет удаляемых объектов
                self.__to_delete_platforms = []
                self.__to_delete_illusionary = []
                self.__to_delete_breakable = []

            # Отрисовка персонажа
            self.__player.update(player_jump, self.__platforms, self.__illusionary, self.__breakable)

            # Отрисовка блоков(это заставляет их двигаться)
            for p in self.__platforms:
                p.update(self.__level_difficult)
            for i in self.__illusionary:
                i.update(self.__level_difficult)
            for b in self.__breakable:
                b.update(self.__level_difficult)

            screen.blit(bg, (0, 0))  # Отрисовка всей картины каждую итерацию цикла
            camera.update(self.__player)  # Обновление камеры по привязке к игроку

            # Кости игрока
            bones_msg = "Bones: " + str(self.__player.bones)  # Текст сообщения
            font_obj = pygame.font.SysFont("Harrington", 32)  # Шрифт
            text_surface = font_obj.render(bones_msg, True, (255, 255, 255))  # Поверхность с текстом
            text_rect = text_surface.get_rect()  # Получаем область поверхности
            text_rect.center = (100, 50)  # Задаем координаты отображения текста
            screen.blit(text_surface, text_rect)  # Отображаем текст

            # Очки игрока
            self.__player.score += time_counter / 10.0  # Используя счетчик времени копим очки игроку
            if self.__player.score > 3000:  # Увеличиваем сложность уровня с 3000 очков
                self.__level_difficult = 4
            elif self.__player.score > 6000:  # Увеличиваем сложность уровня с 6000 очков
                self.__level_difficult = 6
            score_msg = "Score: " + str(int(self.__player.score))  # Текст сообщения
            font_obj = pygame.font.SysFont("Harrington", 32)  # Шрифт
            text_surface = font_obj.render(score_msg, True, (255, 255, 255))  # Поверхность с текстом
            text_rect = text_surface.get_rect()  # Получаем область поверхности
            text_rect.center = (100, 100)  # Задаем координаты отображения текста
            screen.blit(text_surface, text_rect)  # Отображаем текст

            # Отрисовываем объекты каждую итерацию
            for e in self.__entities:
                screen.blit(e.image, camera.apply(e))

            pygame.display.update()  # Обновление всего окна игры

    def __draw_level(self, start_position_x, start_position_y, level):
        # Отрисовка уровня по массиву level
        x = start_position_x
        y = start_position_y
        for row in level:
            for col in row:
                if col == "_":
                    # Создание и заливка блока
                    pf = Block(x, y, "rock")
                    self.__entities.add(pf)
                    self.__platforms.append(pf)
                elif col == "#":
                    # Создание и заливка блока
                    pf = Block(x, y, "dirt")
                    self.__entities.add(pf)
                    self.__platforms.append(pf)
                elif col == "@":
                    pf = Block(x, y, "bone")
                    self.__entities.add(pf)
                    self.__breakable.append(pf)
                elif col == ";":
                    pf = Block(x, y, "grass")
                    self.__entities.add(pf)
                    self.__illusionary.append(pf)
                x += Block.get_block_width()
            y += Block.get_block_height()
            x = start_position_x

    def __clear_level(self):
        self.__entities.remove(self.__platforms)
        self.__entities.remove(self.__illusionary)
        self.__entities.remove(self.__breakable)
        for i in xrange(len(self.__platforms)):
            self.__platforms.__delitem__(0)
        for i in xrange(len(self.__breakable)):
            self.__breakable.__delitem__(0)
        for i in xrange(len(self.__illusionary)):
            self.__illusionary.__delitem__(0)
        for i in xrange(len(self.__to_delete_platforms)):
            self.__to_delete_platforms.__delitem__(0)
        for i in xrange(len(self.__to_delete_breakable)):
            self.__to_delete_breakable.__delitem__(0)
        for i in xrange(len(self.__to_delete_illusionary)):
            self.__to_delete_illusionary.__delitem__(0)

    @staticmethod
    def camera_configure(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + Launcher.get_window_width() / 2, -t + Launcher.get_window_height() / 2
        l = min(0, l)  # Не движемся дальше левой границы
        l = max(-(camera.width - Launcher.get_window_width()), l)  # Не движемся дальше правой границы
        t = max(-(camera.height - Launcher.get_window_height()), t)  # Не движемся дальше нижней границы
        t = min(0, t)  # Не движемся дальше верхней границы
        return Rect(l, t, w, h)
