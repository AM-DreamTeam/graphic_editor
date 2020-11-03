""" Новые объекты """

# Импортирование модулей
from tkinter import Canvas


class CustomCanvas(Canvas):
    """ CustomCanvas(Canvas) - для того, чтобы не портить canvas из моудля tkinter создадим класс с расширенными полями и методами

        Поля:
            * old_point: None or Tuple[int] - временное хранилище прошлых координат точки
            * obj_oval: None or Oval - временное хранилище эллипса
            * obj_line: None or Line - временное хранилище прямой (отрезка)
            * obj_rectangle: None or Rectangle - временное хранилище прямоугольника
            * obj_storage: dict - хранилище графических примитивов на слое (canvas'e)
    """

    old_point = None

    obj_oval = None
    obj_line = None
    obj_rectangle = None

    obj_storage = {}