# Импортирование модулей
from tkinter import Canvas


class CustomCanvas(Canvas):
    """ CustomCanvas(Canvas) - для того, чтобы не портить canvas из моудля tkinter создадим класс с расширенными полями и методами

        Поля:
            * obj_ovals - временное хранилище овалов
            * obj_lines - временное хранилище прямых
    """

    obj_ovals = []
    obj_lines = []