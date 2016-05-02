#!/usr/bin/env python
# coding=utf-8

import random
from pygame import *
from Zones import *
from Camera import *
from Player import *
from Block import Block
from Intro import Intro


class Game(object):
    def __init__(self):
        self.__game_music = "sounds/game.wav"  # Путь к музыке
        self.__player = Player(100, 100)  # Создание игрока
        self.__game_difficult = 3  # Уровень сложности
        self.__min_height = 868  # Минимальная высота, после нее игрок умирает
        self.__best_score = 0  # Рекорд игрока
        self.__entities = pygame.sprite.Group()  # Создаем группу для объектов
        self.__platforms = []  # То, что может служить опорой или барьером
        self.__to_delete_platforms = []  # Платформы, которые нужно будет удалить
        self.__illusionary = []  # То, через что можно пройти и оно не исчезнет
        self.__to_delete_illusionary = []
        self.__breakable = []  # То, через что можно пройти и оно исчезнет
        self.__to_delete_breakable = []

    def start_game(self, screen, bg, window_width, window_height):
        self.__entities.add(self.__player)  # Добавляем в объекты игрока
        player_jump = False  # Изначально игрок не прыгает
        checkpoint = 0  # По достижение опр. кол-ва очков, очки игрока сохраняются сюда
        self.__draw_level(0, 0, start_zone)  # Отрисовываем уровень
        timer = pygame.time.Clock()  # Временной счетчик

        # Фон
        moon_position = window_width - 142  # Начальная позицияя луны
        mountains_position = 0  # Начальная позиция гор
        mountains = self.__generate_mountain_coordinates(bg)  # Начальная генерация гор

        music = pygame.mixer.Sound(self.__game_music)  # Подгружаем музыку
        if Intro.check_sound():
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
                self.__game_difficult = 3  # При каждом оживлении обнуляем уровень сложности
                time_counter = 0  # При каждом оживлении обнуляем временной счетчик
                checkpoint = 0  # Обнуляем чекпоинт

            # Фон
            bg.fill(Color("#6C8784"))  # Заполняем фон сплошным цветом
            # Луна
            moon_position -= time_counter / 17  # Двигаем луну засчет изменения позиции
            if moon_position + 200 < 0:  # Если луна ушла за пределы, то переместить ее в другой конец
                moon_position = window_width + 100
            pygame.draw.circle(bg, (210, 215, 211), [moon_position, 154], 100)  # Отрисовка луны
            # Горы
            mountains_position -= time_counter / 10  # Двигаем горы засчет изменения позиции
            if mountains_position + bg.get_width() * 2 < 0:  # Если горы ушли за пределы, то переместить их в другой конец
                mountains_position = 0
                mountains = self.__generate_mountain_coordinates(bg)
            for i in xrange(3):  # Отрисовка гор
                pygame.draw.polygon(bg, (37, 55, 61), [
                    [mountains[i][0][0] + mountains_position, mountains[i][0][1]],
                    [mountains[i][1][0] + mountains_position, mountains[i][1][1]],
                    [mountains[i][2][0] + mountains_position, mountains[i][2][1]]
                ])

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
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    # Удаляем все объекты
                    self.__entities.remove(self.__to_delete_platforms)
                    self.__entities.remove(self.__to_delete_illusionary)
                    self.__entities.remove(self.__to_delete_breakable)
                    self.__entities.remove(self.__platforms)
                    self.__entities.remove(self.__illusionary)
                    self.__entities.remove(self.__breakable)
                    self.__to_delete_platforms = []
                    self.__to_delete_illusionary = []
                    self.__to_delete_breakable = []
                    self.__platforms = []
                    self.__illusionary = []
                    self.__breakable = []
                    self.__player.rect.x = self.__player.start_position_x
                    self.__player.rect.y = self.__player.start_position_y
                    self.__player.score = 0
                    if Intro.check_sound():
                        music.stop()
                    return
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
            elif len(self.__to_delete_platforms) != 0 and self.__to_delete_platforms[
                        len(self.__to_delete_platforms) - 1].rect.x < -10:
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
            self.__player.update(player_jump, self.__game_difficult, self.__platforms, self.__illusionary,
                                 self.__breakable)

            # Смерть игрока при падении вниз
            if self.__player.rect.y > self.__min_height or self.__player.rect.x < -self.__player.get_player_width() * 3:
                if self.__player.score > self.__best_score:
                    self.__best_score = self.__player.score
                self.__player.die()

            # Отрисовка блоков(это заставляет их двигаться)
            for p in self.__platforms:
                p.update(self.__game_difficult)
            for i in self.__illusionary:
                i.update(self.__game_difficult)
            for b in self.__breakable:
                b.update(self.__game_difficult)

            screen.blit(bg, (0, 0))  # Отрисовка всей картины каждую итерацию цикла
            camera.update(self.__player, window_width, window_height)  # Обновление камеры по привязке к игроку
            self.__print_gameinfo(screen, bg, time_counter)  # Выводит на экран текстовую информацию
            if int(self.__player.score) - checkpoint == 4000:  # Каждые 4000 увеличивать сложность
                checkpoint = self.__player.score
                self.__game_difficult += 1

            # Отрисовываем объекты каждую итерацию
            for e in self.__entities:
                screen.blit(e.image, camera.apply(e))

            pygame.display.update()  # Обновление всего окна игры

    @staticmethod
    def __generate_mountain_coordinates(bg):
        mountains = []

        first_mountain_left_dot = [bg.get_width(), bg.get_height()]
        first_mountain_top_dot = [first_mountain_left_dot[0] + random.randint(50, 130),
                                  random.randint(bg.get_height()/8, bg.get_height()/2)]
        first_mountain_right_dot = [first_mountain_top_dot[0] + random.randint(50, 320), bg.get_height()]
        mountains.append([first_mountain_top_dot, first_mountain_right_dot, first_mountain_left_dot])

        second_mountain_left_dot = [first_mountain_right_dot[0] - random.randint(0, first_mountain_right_dot[0] - first_mountain_left_dot[0]),
                                    first_mountain_right_dot[1]]
        second_mountain_top_dot = [second_mountain_left_dot[0] + random.randint(50, 130),
                                   random.randint(bg.get_height()/8, bg.get_height()/2)]
        second_mountain_right_dot = [second_mountain_top_dot[0] + random.randint(50, 320), bg.get_height()]
        mountains.append([second_mountain_top_dot, second_mountain_right_dot, second_mountain_left_dot])

        third_mountain_left_dot = [second_mountain_right_dot[0] - random.randint(0, second_mountain_right_dot[0] - second_mountain_left_dot[0]), second_mountain_right_dot[1]]
        third_mountain_top_dot = [third_mountain_left_dot[0] + random.randint(50, 130),
                                  random.randint(bg.get_height()/8, bg.get_height()/2)]
        third_mountain_right_dot = [third_mountain_top_dot[0] + random.randint(50, 320), bg.get_height()]
        mountains.append([third_mountain_top_dot, third_mountain_right_dot, third_mountain_left_dot])
        return mountains

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

    def __print_gameinfo(self, screen, bg, time_counter):
        best_font = pygame.font.SysFont("Harrington", 36)  # Шрифт рекорда
        score_font = pygame.font.SysFont("Harrington", 64)  # Шрифт очков
        # Очки игрока
        self.__player.score += time_counter / 10  # Используя счетчик времени копим очки игроку
        score_msg = str(self.__player.score)  # Текст сообщения
        score_surface = score_font.render(score_msg, True, (255, 255, 255))  # Поверхность с текстом
        score_rect = score_surface.get_rect()  # Получаем область поверхности
        score_rect.center = (bg.get_width()/2, 200)  # Задаем координаты отображения текста
        screen.blit(score_surface, score_rect)  # Отображаем текст

        # Рекорд игрока
        if self.__best_score < self.__player.score:
            self.__best_score = self.__player.score
            best_msg_color = [255, 255, 255]
        else:
            best_msg_color = [210, 215, 211]
        best_msg = "Best: " + str(self.__best_score)  # Текст сообщения
        best_surface = best_font.render(best_msg, True, best_msg_color)  # Поверхность с текстом
        best_rect = best_surface.get_rect()  # Получаем область поверхности
        best_rect.x, best_rect.y = 20, 20  # Задаем координаты отображения рекорда
        screen.blit(best_surface, best_rect)  # Отображаем текст

    @staticmethod
    def camera_configure(camera, target_rect, window_width, window_height):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + window_width / 2, -t + window_height / 2
        l = min(0, l)  # Не движемся дальше левой границы
        l = max(-(camera.width - window_width), l)  # Не движемся дальше правой границы
        t = max(-(camera.height - window_height), t)  # Не движемся дальше нижней границы
        t = min(0, t)  # Не движемся дальше верхней границы
        return Rect(l, t, w, h)

    def get_level_difficult(self):
        return self.__game_difficult
