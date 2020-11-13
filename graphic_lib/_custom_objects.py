""" Новые настраиваемые объекты """


# Импортированные модулей
from tkinter import Canvas


class CustomCanvas(Canvas):
    """ CustomCanvas(Canvas) - для того, чтобы не портить canvas из моудля tkinter создадим класс с расширенными полями и методами

        Поля:
            * old_point: None or Tuple[int] - временное хранилище прошлых координат точки
            * obj_oval: None or Oval - временное хранилище эллипса
            * obj_line: None or Line - временное хранилище прямой (отрезка)
            * obj_rectangle: None or Rectangle - временное хранилище прямоугольника
            * line_sequences: list - хранение последовательности линий
            * obj_storage: dict - хранилище графических примитивов на слое (canvas'e)
            * obj_tag: None or str - временное хранилище tag'ов объектов, на которые нажимает пользователь
    """

    old_point = None

    obj_oval = None
    obj_line = None
    obj_rectangle = None

    line_sequences = []
    obj_storage = {}

    obj_tag = None