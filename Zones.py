#!/usr/bin/env python
# coding=utf-8

start_zone = [
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "                         ",
    "g                        ",
    "_____   g           g    ",
    "#####____  g       __    ",
    "  #######______   _##    ",
    "  #############___###__  ",
    "   ###########  #######_ ",
    "       #####      ######_"
]

zones = [
    [
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                g        ",
        "  g             _   __   ",
        "_____  g    __  #        ",
        "  ###___    ##           ",
        "       #                _",
        "                         "
    ],
    [
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "         g           g   ",
        "  g      _     ___   __  ",
        "____   ###   __###       "
    ],
    [
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "            g            ",
        "            _   @__   g  ",
        "           _#   _##   ___",
        "         g_#    ##    #  ",
        "     g   _#              ",
        "    __   #               ",
        "___                      ",
        "                         "
    ],
    [
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "       g       g_     g  ",
        "___    _       _#     _  ",
        "  #__     @  _    __     ",
        "          _       ##     "
    ],
    [
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "        g                ",
        "        __               ",
        "       ###               ",
        "  g  _                   ",
        "___                   _  ",
        "                gg   _   ",
        "               ____      "
    ],
    [
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "        g   _            ",
        "___@g  ___  #   g        ",
        " ##__           __ g   __",
        "   ##           ######  #"
    ],
    [
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        " g                       ",
        " _           g           ",
        "_#_     g   __      g    ",
        "###_g  ___   #   @ __  g_",
        "#####   ##       _     _#"
    ],
    [
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "               __        ",
        "             __##____    ",
        "   __#####    #######____",
        "___########    #     ####"
    ],
    [
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                  __     ",
        "         _     g_@##     ",
        "       __#    g##_##  g  ",
        "   g _ ###g   ######_____",
        "___### ####   ##    #####"
    ]
]


# Чистая заготовка
"""
    [
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         "
    ]
"""
