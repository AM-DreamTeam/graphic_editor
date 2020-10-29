""" Графические примитивы """

# Импортированные модули
from tkinter import *
from _custom_objects import CustomCanvas
from _defaults import *
from typing import List, Tuple
from numpy import subtract


class Basic:
    """ Basic - базовые функции

        Аргументы:
            * root: tkinter.Tk - главное окно

        Методы:
            * unbind_all_events(used_events: List[str]) -> None

        Статические методы:
            * transform_coords(old_coords: Tuple[int], new_coords: Tuple[int]) -> Tuple[int]
    """

    def __init__(self, root: Tk):
        self._root = root

    def unbind_all_events(self, used_events: List[str]) -> None:
        """ Очищает все действующие бинды

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды - used_events
        """

        for _ in used_events:
            self._root.unbind(_)

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


class Draw:
    """ Draw - отрисовка элементов

        Статические методы:
            * point(event: Event, canvas: Canvas, *, size: int = 5, color: str = 'black') -> None
            * oval(event: Event, canvas: Canvas, thickness: int = 2, bgcolor: str, outcolor: str) -> None
            * line(event: Event, canvas: Canvas, thickness: int = 2, bgcolor: str = None, outcolor: str = 'black') -> None
            * rectangle(event: Event, canvas: Canvas, thickness: int = 2, bgcolor: str = None, outcolor: str = 'black') -> None
    """

    @staticmethod
    def point(event: Event, canvas: Canvas,
               *,
               size: int = 5,
               color: str = 'black') -> None:
        """ Рисует точку на месте курсора

            Аргументы:
                * event: tkinter.Event - событие, по которому считываем положение курсора
                * canvas: tkinter.Canvas - canvas (слой), на котором рисуем точку
                ** size: int - размер точки (овала)
                ** color: str - цвет точки (овала)

            Возвращает:
                None

            Побочный эффект:
                Отрисовка точки (овала) на canvas'e (слое)
        """

        x1, y1 = event.x - 1, event.y - 1
        x2, y2 = event.x + 1, event.y + 1

        canvas.create_oval(x1, y1, x2, y2, fill=color, width=size)

    # TODO: добавить параметр dash
    @staticmethod
    def line(event: Event, canvas: CustomCanvas,
             *,
             thickness: int = 2,
             color: str = 'black') -> None:
        """ Рисует линию по заданным точкам

             Аргументы:
                * event: tkinter.Event - событие, по которому считывается положение курсора
                * canvas: tkinter.Canvas - canvas (слой), на котором рисуем прямую
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
        elif str(event.type) == 'ButtonRelease':
            x1, y1 = new_point
            x2, y2 = canvas.old_point
            canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color)
        elif str(event.type) == 'Motion':
            x1, y1 = new_point
            x2, y2 = canvas.old_point
            l = canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color)

            if canvas.obj_line:
                canvas.delete(canvas.obj_line)

            canvas.obj_line = l

    # TODO: добавить параметр dash
    @staticmethod
    def oval(event: Event, canvas: Canvas,
             *,
             thickness: int = 2,
             bgcolor: str = None,
             outcolor: str = 'black') -> None:
        """ Рисует эллипс по заданным точкам

            Аргументы:
                * event: tkinter.Event - событие, по которому считавается положение курсора
                * canvas: tkinter.Canvas - canvas (слой), на котором рисуем эллипс
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
        elif str(event.type) == 'ButtonRelease':
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if event.state == 260 else new_point
            x2, y2 = canvas.old_point
            canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)
        elif str(event.type) == 'Motion':
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if event.state == 260 else new_point
            x2, y2 = canvas.old_point
            o = canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)

            if canvas.obj_oval:
                canvas.delete(canvas.obj_oval)

            canvas.obj_oval = o

    # TODO: добавить параметр dash
    @staticmethod
    def rectangle(event: Event, canvas: Canvas,
             *,
             thickness: int = 2,
             bgcolor: str = None,
             outcolor: str = 'black') -> None:
        """ Рисует прямоугольник по заданным точкам

            Аргументы:
                * event: tkinter.Event - событие, по которому считавается положение курсора
                * canvas: tkinter.Canvas - canvas (слой), на котором рисуем прямоугольник
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
        elif str(event.type) == 'ButtonRelease':
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if event.state == 260 else new_point
            x2, y2 = canvas.old_point
            canvas.create_rectangle(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)
            canvas.delete(canvas.obj_rectangle)
        elif str(event.type) == 'Motion':
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

        Методы:
            * event_btnClear(used_events: List[str], canvas: Canvas) -> None
            * event_btnBrush_Event(used_events: List[str], canvas: Canvas, *, size: int = 5, color: str = 'black') -> None
            * event_btnCreateLine(used_events: List[str], canvas: Canvas, *, thickness: int = 2, color: str = 'black') -> None
            * event_btnCreateOval(used_events: List[str], canvas: Canvas, *, thickness: int = 2, bgcolor: str = None, outcolor: str = 'black') -> None
            * event_btnCreateRectangle(used_events: List[str], canvas: Canvas, *, thickness: int = 2, bgcolor: str = None, outcolor: str = 'black') -> None
    """

    def __init__(self, root: Tk):
        self._root = root
        self._Basic = Basic(root)

    def event_btnClear(self, used_events: List[str], canvas: Canvas) -> None:
        """ Событие для кнопки btnClear

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий
                * canvas: tkinter.Canvas - canvas (слой), который очищается

            Возвращает:
                None

            Побочный эффект:
                Очистка canvas'a (слоя)
        """

        self._Basic.unbind_all_events(used_events)
        canvas.delete('all')

    def event_btnBrush(self, used_events: List[str], canvas: Canvas,
                  *,
                  size: int = 5,
                  color: str = 'black') -> None:
        """ Событие для кнопки btnBrush

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий
                * canvas: tkinter.Canvas - canvas (слой), на котором будет отрисовываться последовательность точек (овалов)
                ** size: int - размер точки (овала)
                ** color: str - цвет точки (овала)

            Возвращает:
                None

            Побочный эффект:
                Очищаются все бинды и создаётся новый бинд на <B1-Motion> - отрисовка последовательности точек (овалов)
        """

        self._Basic.unbind_all_events(used_events)

        self._root.bind('<B1-Motion>', lambda event, c=canvas, s=size, clr=color: Draw.point(event, canvas,
                                                                                        size=s,
                                                                                        color=clr))

    def event_btnCreateLine(self, used_events: List[str], canvas: Canvas,
                            *,
                           thickness: int = 2,
                           color: str = 'black') -> None:
        """ Событие для кнопки btnCreateLine

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий
                * canvas: tkinter.Canvas - canvas (слой), на котором будет отрисовываться линия (отрезок)
                ** thickness: int - жирность линии
                ** color: str - цвет линии

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 3 новых бинла <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion> - отрисовка линии (отрезка)
        """

        self._Basic.unbind_all_events(used_events)

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>'):
            self._root.bind(event, lambda event, c=canvas, t=thickness, clr=color: Draw.line(event, c,
                                                                                       thickness=t,
                                                                                       color=clr))

    def event_btnCreateOval(self, used_events: List[str], canvas: Canvas,
                            *,
                            thickness: int = 2,
                            bgcolor: str = None,
                            outcolor: str = 'black') -> None:
        """ Событие для кнопки btnCreateOval

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий
                * canvas: tkinter.Canvas - canvas (слой), на котором рисуем эллипс
                ** thickness: int - жирность обводки эллипса
                ** bgcolor: str - цвет заливки эллипса
                ** outcolor: str - цвет обводки эллипса

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 3 новых бинла <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion> - отрисовка эллипса
        """

        self._Basic.unbind_all_events(used_events)

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>'):
            self._root.bind(event, lambda event, c=canvas, t=thickness, bgclr=bgcolor, outclr=outcolor: Draw.oval(event, c,
                                                                                                    thickness=t,
                                                                                                    bgcolor=bgclr,
                                                                                                    outcolor=outclr))

    def event_btnCreateRectangle(self, used_events: List[str], canvas: Canvas,
                            *,
                            thickness: int = 2,
                            bgcolor: str = None,
                            outcolor: str = 'black') -> None:
        """ Событие для кнопки btnCreateOval

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий
                * canvas: tkinter.Canvas - canvas (слой), на котором рисуем прямоугольник
                ** thickness: int - жирность обводки прямоугольника
                ** bgcolor: str - цвет заливки прямоугольника
                ** outcolor: str - цвет обводки прямоугольника

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 3 новых бинла <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion> - отрисовка прямоугольника
        """

        self._Basic.unbind_all_events(used_events)

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>', '<KeyPress-Control_L>', '<KeyRelease-Control_L>'):
            self._root.bind(event, lambda event, c=canvas, t=thickness, bgclr=bgcolor, outclr=outcolor: Draw.rectangle(event, c,
                                                                                                            thickness=t,
                                                                                                            bgcolor=bgclr,
                                                                                                            outcolor=outclr))


# Создаём пример приложения
if __name__ == '__main__':

    # Тестируем все доктесты
    import doctest
    doctest.testmod()


    class App:
        """ App - пример приложение для проверки модуля """

        def __init__(self, root):
            root.title('Graphic Basic')

            events = Events(root)

            frame_main = Frame(root)
            frame_main.pack()

            canvas = CustomCanvas(frame_main, width=CANVAS_W, height=CANVAS_H, bg=CANVAS_BG)
            canvas.pack(side=RIGHT)

            btnClear = Button(frame_main, text='*отчистить*',
                              command=lambda ue=USED_EVENTS, c=canvas: events.event_btnClear(ue, c))
            btnClear.pack(side=TOP, pady=5)

            btnBrush = Button(frame_main, text='*кисть*',
                              command=lambda ue=USED_EVENTS, c=canvas, s=SIZE, clr=FIRST_COLOR:
                              events.event_btnBrush(ue, c, size=s, color='black'))
            btnBrush.pack(side=TOP, pady=5)

            btnCreateLine = Button(frame_main, text='*линия*',
                                   command=lambda ue=USED_EVENTS, c=canvas, t=THICKNESS, clr=FIRST_COLOR:
                                   events.event_btnCreateLine(ue, c, thickness=t, color=clr))
            btnCreateLine.pack(side=TOP, pady=5)

            btnCreateOval = Button(frame_main, text='*эллипс*',
                                   command=lambda ue=USED_EVENTS, c=canvas, t=THICKNESS, outclr=FIRST_COLOR, bgclr=SECOND_COLOR:
                                   events.event_btnCreateOval(ue, c, thickness=t, bgcolor=bgclr, outcolor=outclr))
            btnCreateOval.pack(side=TOP, pady=5)

            btnCreateRectangle = Button(frame_main, text='*прямоугольник*',
                                   command=lambda ue=USED_EVENTS, c=canvas, t=THICKNESS, outclr=FIRST_COLOR, bgclr=SECOND_COLOR:
                                   events.event_btnCreateRectangle(ue, c, thickness=t, bgcolor=bgclr, outcolor=outclr))
            btnCreateRectangle.pack(side=TOP, pady=5)

            root.bind('<Control-x>', quit)


    root = Tk()
    App(root)
    root.mainloop()