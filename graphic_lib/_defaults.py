"""
    Стандартные настройки

    USED_EVENTS - события, которые используются

    FIRST_COLOR - основной цвет или цвет обводки для графического примитива
    SECOND_COLOR - дополнительный цвет (цвет заливки) для графического примитива
    SIZE - размер кисти
    THICKNESS - ширина обводки графического примитива

    CANVAS_W - ширина слоя (canvas'a)
    CANVAS_H - высота слоя (canvas'a)
    CANVAS_BG - заливка слоя (canvas'a)
"""

USED_EVENTS = ('<B1-Motion>', '<ButtonPress-1>','<ButtonRelease-1>', '<KeyPress-Control_L>', '<KeyRelease-Control_L>')


FIRST_COLOR = 'black'
SECOND_COLOR = None
THICKNESS = 2
SIZE = 5

CANVAS_W = 800
CANVAS_H = 600
CANVAS_BG = 'white'