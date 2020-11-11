""" Базовые функции для реализации графических  примитивов

    reset(function: Callable[..., None]) -> Callable[..., None]
    transform_coords(old_coords: Tuple[int], new_coords: Tuple[int]) -> Tuple[int]
    transform_line_coords(old_coords: Tuple[int], new_coords: Tuple[int]) -> Tuple[int]
    detect_object(event: tkinter.Event, _custom_objetcs.CustomCanvas) -> [str, None]
"""


# Имортированные модули
from numpy import subtract


def reset(function):
    """ Декоратор, который очищает бинды и удаляет старые точки

    Аргументы:
        * function: Callable[..., None] - декорируемая фнкция

    Возвращает:
        Callable[..., None] - функцию, с очищенными старыми точками и биндами
    """

    def inner(self, *args, **kwargs):
        self._canvas.old_point = None
        for _ in self._used_events:
            self._root.unbind(_)
        return function(self, *args, **kwargs)
    return inner


def transform_coords(old_coords, new_coords):
    """ Переводит координаты прямоугольного объекта в квадратные

        Аргументы:
            * old_coords: Tuple[int] - кортеж из 2х элементов - координаты стартовой точки
            * new_coords: Tuple[int] - кортеж из 2х элементов - координаты конечной точки

        Возвращает:
            Tuple[int]: преобразованные координаты

        Тесты:
            >>> transform_coords((4, 2), (1, 3))
            (3, 3)

            >>> transform_coords((14, 11), (8, 4))
            (8, 5)

            >>> transform_coords((4, 2), (1, 4))
            (2, 4)
    """

    deltaX, deltaY = tuple(subtract(new_coords, old_coords))

    if deltaX > 0 and deltaY < 0:
        delta = deltaX + deltaY
        return (new_coords[0] - delta, new_coords[1])
    elif deltaX < 0 and deltaY > 0:
        delta = abs(deltaX + deltaY)
        return (new_coords[0] + delta, new_coords[1])
    else:
        delta = abs(deltaX - deltaY)
        return (new_coords[0] + delta, new_coords[1]) if deltaY > deltaX else (new_coords[0], new_coords[1] + delta)


def transform_line_coords(old_coords, new_coords):
    """ Переводит координаты линии в вертикальное или горизонтальное положение

        Аргументы:
            * old_coords: Tuple[int] - кортеж из двух элементов - координаты старой точки
            * new_coords: Tuple[int] - кортеж из двех элеметов - координаты конечной точки

        Возвращает:
            Tuple[int]: преобразованные координаты

        Тесты:
            >>> transform_line_coords((4, 2), (1, 3))
            (1, 2)

            >>> transform_line_coords((14, 11), (8, 4))
            (14, 4)

            >>> transform_line_coords((4, 2), (1, 5))
            (4, 5)
    """

    deltaX, deltaY = tuple(subtract(new_coords, old_coords))
    return (new_coords[0], old_coords[1]) if abs(deltaX) > abs(deltaY) else (old_coords[0], new_coords[1])


def detect_object(event, canvas):
    """ Определяет tag объекта, на который нажимает пользователь

        Аргументы:
            * event: tkinter.Event - событие, по которому считываем  положение курсора
            * canvas: _custom_objetcs.CustomCanvas - canvas (слой), на котором находятся объекты


        Возвращает:
            str or None: tag объекта, по которому нажал пользователь
    """

    x, y = event.x, event.y
    storage = canvas.obj_storage

    obj, coords = list(storage.keys()), list(storage.values())
    obj_lst = []

    for obj_coords in coords:
        x1, y1, x2, y2 = obj_coords
        if (x1 > x > x2 or x2 > x > x1) and (y1 > y > y2 or y2 > y > y1):
            obj_lst.append(obj[coords.index(obj_coords)])

    return obj_lst[-1] if obj_lst else None


if __name__ == '__main__':
    import doctest
    doctest.testmod()