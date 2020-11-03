""" Стандартные настройки

    USED_EVENTS - события, которые используются

    FIRST_COLOR - основной цвет или цвет обводки для графического примитива
    SECOND_COLOR - дополнительный цвет (цвет заливки) для графического примитива
    SIZE - размер кисти
    THICKNESS - ширина обводки графического примитива

    CANVAS_W - ширина слоя (canvas'a)
    CANVAS_H - высота слоя (canvas'a)
    CANVAS_BG - заливка слоя (canvas'a)
"""

DEFAULT_USED_EVENTS = ('<B1-Motion>', '<ButtonPress-1>','<ButtonRelease-1>', '<KeyPress-Control_L>', '<KeyRelease-Control_L>')

DEFAULT_FIRST_COLOR = 'black'
DEFAULT_SECOND_COLOR = None
DEFAULT_THICKNESS = 2
DEFAULT_SIZE = 5

DEFAULT_CANVAS_W = 800
DEFAULT_CANVAS_H = 600
DEFAULT_CANVAS_BG = 'white'