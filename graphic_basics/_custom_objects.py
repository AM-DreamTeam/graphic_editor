# Импортирование модулей
from tkinter import Canvas


class CustomCanvas(Canvas):
    """ CustomCanvas(Canvas) - для того, чтобы не портить canvas из моудля tkinter создадим класс с расширенными полями и методами

        Поля:
            * old_point - временное хранилище прошлых координат точки
            * obj_oval - временное хранилище эллипса
            * obj_line - временное хранилище прямой (отрезка)
            * obg_rectangle - временное хранилище прямоугольника
    """

    old_point = None
    obj_oval = None
    obj_line = None
    obj_rectangle = None