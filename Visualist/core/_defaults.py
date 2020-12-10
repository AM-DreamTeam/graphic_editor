""" Стандартные настройки

    DEFAULT_USED_EVENTS - события, которые используются

    DEFAULT_FIRST_COLOR - основной цвет или цвет обводки для графического примитива
    DEFAULT_SECOND_COLOR - дополнительный цвет (цвет заливки) для графического примитива
    DEFAULT_CHANGE_COLOR - цвет графического примитива при его смене на прошлый
    DEFAULT_BRUSH_SIZE - размер кисти
    DEFAULT_ERASER_SIZE - размер ластика
    DEFAULT_THICKNESS - ширина обводки графического примитива

    DEFAULT_MOUSE_SPEED - скорость передвижения объектов на слое (canvas'e)

    DEFAULT_CANVAS_W - ширина слоя (canvas'a)
    DEFAULT_CANVAS_H - высота слоя (canvas'a)
    DEFAULT_CANVAS_BG - заливка слоя (canvas'a)
"""


""" ============= graphic_lib ============ """


DEFAULT_USED_EVENTS = ('<B1-Motion>',
                       '<ButtonPress-1>',
                       '<ButtonRelease-1>',
                       '<KeyPress-Control_L>',
                       '<KeyRelease-Control_L>')

DEFAULT_FIRST_COLOR = 'black'
DEFAULT_SECOND_COLOR = ''
DEFAULT_CHANGE_COLOR = 'green'
DEFAULT_THICKNESS = 2
DEFAULT_BRUSH_SIZE = 5
DEFAULT_ERASER_SIZE = 20

DEFAULT_MOUSE_SPEED = 5

DEFAULT_CANVAS_W = 800
DEFAULT_CANVAS_H = 600
DEFAULT_CANVAS_BG = 'white'


""" ============= image_lib ============ """


DEFAULT_FILTERS_1 = [
                    "размытие",
                    "размытие",
                    "контур",
                    "резкость",
                    "рельеф",
                    "выделение краев",
                    "сглаживание"
                    ]

DEFAULT_FILTERS_2 = [
                    "насыщенность",
                    "насыщенность",
                    "контрастность",
                    "яркость",
                    "острота"
                    ]

DEFAULT_FILTERS_3 = [
                    "негатив",
                    "негатив",
                    "оттенки серого",
                    "соляризация"
                    ]
