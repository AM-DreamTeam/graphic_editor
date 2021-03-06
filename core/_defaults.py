""" Стандартные настройки

    # graphic_lib
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

    # image_lib
        DEFAULT_FILTERS_1 - список фильтров из 1 группы
        DEFAULT_FILTERS_2 - список фильтров из 2 группы
        DEFAULT_FILTERS_3 - список фильтров из 3 группы
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
                    "Размытие",
                    "Размытие",
                    "Контур",
                    "Резкость",
                    "Рельеф",
                    "Выделение краев",
                    "Сглаживание"
                    ]

DEFAULT_FILTERS_2 = [
                    "Насыщенность",
                    "Насыщенность",
                    "Контрастность",
                    "Яркость",
                    "Острота"
                    ]

DEFAULT_FILTERS_3 = [
                    "Негатив",
                    "Негатив",
                    "Оттенки серого",
                    "Соляризация"
                    ]
