""" Графические примитивы """

# Импортированные модули
from tkinter import *
from _custom_objects import CustomCanvas
from _defaults import *
from typing import List, Tuple, Callable
from numpy import subtract


class Basic:
    """ Basic - базовые функции

        Статические методы:
            * reset(function: Callable[..., None]) -> Callable[..., None]
            * transform_coords(old_coords: Tuple[int], new_coords: Tuple[int]) -> Tuple[int]
            * transform_line_coords(old_coords: Tuple[int], new_coords: Tuple[int]) -> Tuple[int]
    """

    @staticmethod
    def reset(function: Callable[..., None]) -> Callable[..., None]:
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

    @staticmethod
    def transform_coords(old_coords: Tuple[int], new_coords: Tuple[int]) -> Tuple[int]:
        """ Переводит координаты прямоугольного объекта в квадратные

            Аргументы:
                * old_coords: Tuple[int] - кортеж из 2х элементов - координаты стартовой точки
                * new_coords: Tuple[int] - кортеж из 2х элементов - координаты конечной точки

            Возвращает:
                Tuple[int]: преобразованные координаты

            Тесты:
                >>> Basic.transform_coords((4, 2), (1, 3))
                (3, 3)

                >>> Basic.transform_coords((14, 11), (8, 4))
                (8, 5)

                >>> Basic.transform_coords((4, 2), (1, 4))
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

    @staticmethod
    def transform_line_coords(old_coords: Tuple[int], new_coords: Tuple[int]) -> Tuple[int]:
        """ Переводит координаты линии в вертикальное или горизонтальное положение

            Аргументы:
                * old_coords: Tuple[int] - кортеж из двух элементов - координаты старой точки
                * new_coords: Tuple[int] - кортеж из двех элеметов - координаты конечной точки

            Возвращает:
                Tuple[int]: преобразованные координаты

            Тесты:
                >>> Basic.transform_line_coords((4, 2), (1, 3))
                (1, 2)

                >>> Basic.transform_line_coords((14, 11), (8, 4))
                (14, 4)

                >>> Basic.transform_line_coords((4, 2), (1, 5))
                (4, 5)
        """

        deltaX, deltaY = tuple(subtract(new_coords, old_coords))

        return (new_coords[0], old_coords[1]) if abs(deltaX) > abs(deltaY) else (old_coords[0], new_coords[1])

class Draw:
    """ Draw - отрисовка элементов

        Статические методы:
            * point(event: Event, canvas: CustomCanvas, *, size: int = 5, color: str = 'black') -> None
            * oval(event: Event, canvas: CustomCanvas, thickness: int = 2, bgcolor: str, outcolor: str) -> None
            * line(event: Event, canvas: CustomCanvas, thickness: int = 2, bgcolor: str = None, outcolor: str = 'black') -> None
            * rectangle(event: Event, canvas: CustomCanvas, thickness: int = 2, bgcolor: str = None, outcolor: str = 'black') -> None
    """

    @staticmethod
    def point(event: Event, canvas: CustomCanvas,
              *,
              size: int = 5,
              color: str = 'black') -> None:
        """ Рисует точку на месте курсора

            Аргументы:
                * event: tkinter.Event - событие, по которому считываем положение курсора
                * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором рисуем отрезок
                ** size: int - размер точки (отрезок)
                ** color: str - цвет точки (отрезок)

            Возвращает:
                None

            Побочный эффект:
                Отрисовка точки (отрезок) на canvas'e (слое)
        """

        x1, y1 = event.x, event.y

        if str(event.type) == 'ButtonRelease':
            canvas.old_point = None
        elif str(event.type) == 'Motion':
            if canvas.old_point:
                x2, y2 = canvas.old_point
                canvas.create_line(x1, y1, x2, y2, width=size, fill=color, smooth=TRUE, capstyle=ROUND)
            canvas.old_point = x1, y1

    # TODO: добавить параметр dash
    @staticmethod
    def line(event: Event, canvas: CustomCanvas,
             *,
             thickness: int = 2,
             color: str = 'black') -> None:
        """ Рисует линию по заданным точкам

             Аргументы:
                * event: tkinter.Event - событие, по которому считывается положение курсора
                * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором рисуем прямую
                ** thickness: int - жирность линии (отрезка)
                ** color: str - цвет линии (отрезка)

            Возвращает:
                None

            Побочный эффект:
                Отрисовка линии по заданным точкам на canvas'e
        """

        new_point = (event.x, event.y)

        if str(event.type) == 'ButtonPress':
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point:
            x2, y2 = canvas.old_point
            x1, y1 = Basic.transform_line_coords(canvas.old_point, new_point) if event.state == 260 else new_point
            canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color, smooth=TRUE, capstyle=ROUND)
        elif str(event.type) == 'Motion' and canvas.old_point:
            x2, y2 = canvas.old_point
            x1, y1 = Basic.transform_line_coords(canvas.old_point, new_point) if event.state == 260 else new_point
            l = canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color, smooth=TRUE, capstyle=ROUND)

            if canvas.obj_line:
                canvas.delete(canvas.obj_line)

            canvas.obj_line = l

    # TODO: добавить параметр dash
    @staticmethod
    def oval(event: Event, canvas: CustomCanvas,
             *,
             thickness: int = 2,
             bgcolor: str = None,
             outcolor: str = 'black') -> None:
        """ Рисует эллипс по заданным точкам

            Аргументы:
                * event: tkinter.Event - событие, по которому считавается положение курсора
                * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором рисуем эллипс
                ** thickness: int - жирность обводки эллипса
                ** bgcolor: str - цвет заливки эллипса
                ** outcolor: str - цвет обводки эллипса

            Возвращает:
                None

            Побочный эффект:
                Отрисовка эллипса по заданным точкам на canvas'е
        """

        new_point = (event.x, event.y)

        if str(event.type) == 'ButtonPress':
            canvas.old_point = event.x, event.y
        elif str(event.type) == 'ButtonRelease' and canvas.old_point:
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if event.state == 260 else new_point
            x2, y2 = canvas.old_point
            canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)
        elif str(event.type) == 'Motion' and canvas.old_point:
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if event.state == 260 else new_point
            x2, y2 = canvas.old_point
            o = canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)

            if canvas.obj_oval:
                canvas.delete(canvas.obj_oval)

            canvas.obj_oval = o

    # TODO: добавить параметр dash
    @staticmethod
    def rectangle(event: Event, canvas: CustomCanvas,
                  *,
                  thickness: int = 2,
                  bgcolor: str = None,
                  outcolor: str = 'black') -> None:
        """ Рисует прямоугольник по заданным точкам

            Аргументы:
                * event: tkinter.Event - событие, по которому считавается положение курсора
                * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором рисуем прямоугольник
                ** thickness: int - жирность обводки прямоугольник
                ** bgcolor: str - цвет заливки прямоугольник
                ** outcolor: str - цвет обводки прямоугольник

            Возвращает:
                None

            Побочный эффект:
                Отрисовка прямоугольника по заданным точкам на canvas'е
        """

        new_point = (event.x, event.y)

        if str(event.type) == 'ButtonPress':
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point:
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if event.state == 260 else new_point
            x2, y2 = canvas.old_point
            canvas.create_rectangle(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)
            canvas.delete(canvas.obj_rectangle)
        elif str(event.type) == 'Motion' and canvas.old_point:
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if event.state == 260 else new_point
            x2, y2 = canvas.old_point
            r = canvas.create_rectangle(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)

            if canvas.obj_rectangle:
                canvas.delete(canvas.obj_rectangle)

            canvas.obj_rectangle = r


class Events:
    """ Events - содержит все события

        Аргументы:
            * root: tkinter.Tk - главное окно
            * used_Events: Tuple[str] - список событий
            * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором происходит отрисовка

        Методы:
            * event_btnClear() -> None
            * event_btnBrush_Event(*, size: int = 5, color: str = 'black') -> None
            * event_btnCreateLine(*, thickness: int = 2, color: str = 'black') -> None
            * event_btnCreateOval(*, thickness: int = 2, bgcolor: str = None, outcolor: str = 'black') -> None
            * event_btnCreateRectangle(*, thickness: int = 2, bgcolor: str = None, outcolor: str = 'black') -> None
    """

    def __init__(self, root: Tk, used_events: Tuple[str], canvas: CustomCanvas):
        self._root = root
        self._Draw = Draw
        self._used_events = used_events
        self._canvas = canvas

    __basic = Basic()

    @__basic.reset
    def event_btnClear(self) -> None:
        """ Событие для кнопки btnClear

            Возвращает:
                None

            Побочный эффект:
                Очистка canvas'a (слоя)
        """

        self._canvas.delete('all')

    @__basic.reset
    def event_btnBrush(self,
                       *,
                       size: int = 5,
                       color: str = 'black') -> None:
        """ Событие для кнопки btnBrush

            Аргументы:
                ** size: int - размер точки (овала)
                ** color: str - цвет точки (овала)

            Возвращает:
                None

            Побочный эффект:
                Очищаются все бинды и создаётся новый бинды на <ButtonRelease-1>,  <B1-Motion> - отрисовка
                                                                                    последовательности точек (овалов)
        """

        for event in ('<ButtonRelease-1>', '<B1-Motion>'):
            self._root.bind(event, lambda e, c=self._canvas, s=size, clr=color:
                            self._Draw.point(e, c, size=s, color=clr))

    @__basic.reset
    def event_btnCreateLine(self,
                            *,
                            thickness: int = 2,
                            color: str = 'black') -> None:
        """ Событие для кнопки btnCreateLine

            Аргументы:
                ** thickness: int - жирность линии
                ** color: str - цвет линии

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 3 новых бинла <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                <KeyPress-Control_L>, <KeyRelease-Control_L> - отрисовка линии (отрезка)
        """

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>', '<KeyPress-Control_L>','<KeyRelease-Control_L>'):
            self._root.bind(event, lambda e, c=self._canvas, t=thickness, clr=color:
                            self._Draw.line(e, c, thickness=t, color=clr))

    @__basic.reset
    def event_btnCreateOval(self,
                            *,
                            thickness: int = 2,
                            bgcolor: str = None,
                            outcolor: str = 'black') -> None:
        """ Событие для кнопки btnCreateOval

            Аргументы:
                ** thickness: int - жирность обводки эллипса
                ** bgcolor: str - цвет заливки эллипса
                ** outcolor: str - цвет обводки эллипса

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 3 новых бинла <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                        <KeyPress-Control_L>, <KeyRelease-Control_L> - отрисовка эллипса
        """

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>', '<KeyPress-Control_L>', '<KeyRelease-Control_L>'):
            self._root.bind(event, lambda e, c=self._canvas, t=thickness, bgclr=bgcolor, outclr=outcolor:
                            self._Draw.oval(e, c, thickness=t, bgcolor=bgclr, outcolor=outclr))

    @__basic.reset
    def event_btnCreateRectangle(self,
                                 *,
                                 thickness: int = 2,
                                 bgcolor: str = None,
                                 outcolor: str = 'black') -> None:
        """ Событие для кнопки btnCreateOval

            Аргументы:
                ** thickness: int - жирность обводки прямоугольника
                ** bgcolor: str - цвет заливки прямоугольника
                ** outcolor: str - цвет обводки прямоугольника

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 3 новых бинла <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                    <KeyPress-Control_L>, <KeyRelease-Control_L> - отрисовка прямоугольника
        """

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>', '<KeyPress-Control_L>', '<KeyRelease-Control_L>'):
            self._root.bind(event, lambda e, c=self._canvas, t=thickness, bgclr=bgcolor, outclr=outcolor:
                            self._Draw.rectangle(e, c, thickness=t, bgcolor=bgclr, outcolor=outclr))


# Создаём пример приложения
if __name__ == '__main__':
    # Тестируем все доктесты
    import doctest
    doctest.testmod()


    class App:
        """ App - пример приложение для проверки модуля """

        def __init__(self, root):
            root.title('Graphic Basic')

            frame_main = Frame(root)
            frame_main.pack()

            canvas = CustomCanvas(frame_main, width=DEFAULT_CANVAS_W, height=DEFAULT_CANVAS_H, bg=DEFAULT_CANVAS_BG)
            canvas.pack(side=RIGHT)

            events = Events(root, USED_EVENTS, canvas)

            btnClear = Button(frame_main, text='*отчистить*', command=events.event_btnClear)
            btnClear.pack(side=TOP, pady=5)

            btnBrush = Button(frame_main, text='*кисть*',
                                command=lambda s=DEFAULT_SIZE, clr=DEFAULT_FIRST_COLOR:
                                events.event_btnBrush(size=s, color=clr))
            btnBrush.pack(side=TOP, pady=5)

            btnCreateLine = Button(frame_main, text='*линия*',
                                    command=lambda t=DEFAULT_THICKNESS, clr=DEFAULT_FIRST_COLOR:
                                    events.event_btnCreateLine(thickness=t, color=clr))
            btnCreateLine.pack(side=TOP, pady=5)

            btnCreateOval = Button(frame_main, text='*эллипс*',
                                    command=lambda t=DEFAULT_THICKNESS, outclr=DEFAULT_FIRST_COLOR, bgclr=DEFAULT_SECOND_COLOR:
                                    events.event_btnCreateOval(thickness=t, bgcolor=bgclr, outcolor=outclr))
            btnCreateOval.pack(side=TOP, pady=5)

            btnCreateRectangle = Button(frame_main, text='*прямоугольник*',
                                        command=lambda t=DEFAULT_THICKNESS, outclr=DEFAULT_FIRST_COLOR, bgclr=DEFAULT_SECOND_COLOR:
                                        events.event_btnCreateRectangle(thickness=t, bgcolor=bgclr, outcolor=outclr))
            btnCreateRectangle.pack(side=TOP, pady=5)

            root.bind('<Control-x>', quit)


    root = Tk()
    App(root)
    root.mainloop()