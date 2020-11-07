""" Графические примитивы """

# Импортированные модули
import math
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
            * detect_object(event: tkinter.Event, _custom_objetcs.CustomCanvas) -> [str, None]
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

    @staticmethod
    def detect_object(event: Event, canvas: CustomCanvas) -> [str, None]:
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


class Draw:
    """ Draw - отрисовка элементов

        Аргументы:
            * event: tkinter.Event - событие, по которому считывается положение курсора
            * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором происходит отрисовка

        Методы:
            * point(*, size: int = DEFAULT_SIZE, color: str = DEFAULT_FIRST_COLOR) -> None
            * oval(*, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * line(*, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * rectangle(*, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * move(*, mouse_speed: int = DEFAULT_MOUSE_SPEED) -> None
    """

    def __init__(self, event: Event, canvas: CustomCanvas):
        self._event = event
        self._canvas = canvas

    def point(self,
              *,
              size: int = DEFAULT_SIZE,
              color: str = DEFAULT_FIRST_COLOR) -> None:
        """ Рисует точку на месте курсора

            Аргументы:
                ** size: int - размер точки (отрезок)
                ** color: str - цвет точки (отрезок)

            Возвращает:
                None

            Побочный эффект:
                Отрисовка точки (отрезок) на canvas'e (слое)
        """

        event, canvas = self._event, self._canvas

        x1, y1 = event.x, event.y

        if str(event.type) == 'ButtonRelease':
            canvas.old_point = None
        elif str(event.type) == 'Motion':
            if canvas.old_point:
                x2, y2 = canvas.old_point
                canvas.create_line(x1, y1, x2, y2, width=size, fill=color, smooth=TRUE, capstyle=ROUND)
            canvas.old_point = x1, y1

    def line(self,
             *,
             thickness: int = DEFAULT_THICKNESS,
             color: str = DEFAULT_FIRST_COLOR) -> None:
        """ Рисует линию по заданным точкам

             Аргументы:
                ** thickness: int - жирность линии (отрезка)
                ** color: str - цвет линии (отрезка)

            Возвращает:
                None

            Побочный эффект:
                Отрисовка линии по заданным точкам на canvas'e
        """

        event, canvas = self._event, self._canvas

        new_point = event.x, event.y

        if str(event.type) == 'ButtonPress':
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point:
            tag = f'line{len(canvas.obj_storage) + 1}'
            x2, y2 = canvas.old_point
            x1, y1 = Basic.transform_line_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color, smooth=TRUE, capstyle=ROUND, tags=tag)
            canvas.obj_storage[tag] = (x1, y1, x2, y2)
            canvas.delete(canvas.obj_line)
        elif str(event.type) == 'Motion' and canvas.old_point:
            x2, y2 = canvas.old_point
            x1, y1 = Basic.transform_line_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            l = canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color, smooth=TRUE, capstyle=ROUND)

            if canvas.obj_line:
                canvas.delete(canvas.obj_line)

            canvas.obj_line = l

    def oval(self,
             *,
             thickness: int = DEFAULT_THICKNESS,
             bgcolor: str = DEFAULT_SECOND_COLOR,
             outcolor: str = DEFAULT_FIRST_COLOR) -> None:
        """ Рисует эллипс по заданным точкам

            Аргументы:
                ** thickness: int - жирность обводки эллипса
                ** bgcolor: str - цвет заливки эллипса
                ** outcolor: str - цвет обводки эллипса

            Возвращает:
                None

            Побочный эффект:
                Отрисовка эллипса по заданным точкам на canvas'е
        """

        event, canvas = self._event, self._canvas

        new_point = event.x, event.y

        if str(event.type) == 'ButtonPress':
            canvas.old_point = event.x, event.y
        elif str(event.type) == 'ButtonRelease' and canvas.old_point:
            tag = f'oval{len(canvas.obj_storage) + 1}'
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor, tags=tag)
            canvas.obj_storage[tag] = (x1, y1, x2, y2)
            canvas.delete(canvas.obj_oval)
        elif str(event.type) == 'Motion' and canvas.old_point:
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            o = canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)

            if canvas.obj_oval:
                canvas.delete(canvas.obj_oval)

            canvas.obj_oval = o

    def rectangle(self,
                  *,
                  thickness: int = DEFAULT_THICKNESS,
                  bgcolor: str = DEFAULT_SECOND_COLOR,
                  outcolor: str = DEFAULT_FIRST_COLOR) -> None:
        """ Рисует прямоугольник по заданным точкам

            Аргументы:
                ** thickness: int - жирность обводки прямоугольник
                ** bgcolor: str - цвет заливки прямоугольник
                ** outcolor: str - цвет обводки прямоугольник

            Возвращает:
                None

            Побочный эффект:
                Отрисовка прямоугольника по заданным точкам на canvas'е
        """

        event, canvas = self._event, self._canvas

        new_point = event.x, event.y

        if str(event.type) == 'ButtonPress':
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point:
            tag = f'rectangle{len(canvas.obj_storage)+1}'
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            canvas.create_rectangle(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor, tags=tag)
            canvas.obj_storage[tag] = (x1, y1, x2, y2)
            canvas.delete(canvas.obj_rectangle)
        elif str(event.type) == 'Motion' and canvas.old_point:
            x1, y1 = Basic.transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            r = canvas.create_rectangle(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)

            if canvas.obj_rectangle:
                canvas.delete(canvas.obj_rectangle)

            canvas.obj_rectangle = r

    def move(self, *, mouse_speed: int = DEFAULT_MOUSE_SPEED) -> None:
        """ Двигает объекты на canvas'e (слое)

            Аргументы:
                ** mouse_speed: int - скорость передвижения объектов (скорость мыши) на слое (canvas'e)

            Возвращает:
                None

            Побочный эффект:
                Двигает объект на слое (canvas'e) и перезаписывает его координаты
        """

        event, canvas = self._event, self._canvas

        if str(event.type) == 'ButtonPress':
            canvas.obj_tag = Basic.detect_object(event, canvas)
        elif str(event.type) == 'ButtonRelease' and canvas.obj_tag:
            canvas.obj_storage[canvas.obj_tag] = canvas.coords(canvas.obj_tag)
            canvas.obj_tag = None
        elif str(event.type) == 'Motion' and canvas.obj_tag:
            x1, y1, x2, y2 = canvas.coords(canvas.obj_tag)
            obj_center_x, obj_center_y = (x1+x2)/2, (y1+y2)/2
            mouse_x, mouse_y = event.x, event.y

            move_x, move_y = mouse_x-obj_center_x, mouse_y-obj_center_y
            theta = math.atan2(move_y, move_x)
            x, y = mouse_speed*math.cos(theta), mouse_speed*math.sin(theta)

            canvas.move(canvas.obj_tag, x, y)


class Events:
    """ Events - содержит все события

        Аргументы:
            * root: tkinter.Tk - главное окно
            * used_Events: Tuple[str] - список событий
            * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором происходит отрисовка

        Поля:
            * __basic: Basic - экземпляр класса Basic

        Методы:
            * event_btnClear() -> None
            * event_btnBrush_Event(*, size: int = DEFAULT_SIZE, color: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateLine(*, thickness: int = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateOval(*, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateRectangle(*, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * event_undo() -> None
            * event_move(*, mouse_speed: int = DEFAULT_MOUSE_SPEED) -> None
    """

    def __init__(self, root: Tk, used_events: Tuple[str], canvas: CustomCanvas):
        self._root = root
        self._used_events = used_events
        self._canvas = canvas
        self.__draw = lambda e, c: Draw(e, c)

    __basic = Basic()

    @__basic.reset
    def event_btnClear(self) -> None:
        """ Событие для кнопки btnClear

            Возвращает:
                None

            Побочный эффект:
                Очистка canvas'a (слоя)
        """

        self._canvas.obj_storage = {}
        self._canvas.delete('all')

    @__basic.reset
    def event_btnBrush(self,
                       *,
                       size: int = DEFAULT_SIZE,
                       color: str = DEFAULT_FIRST_COLOR) -> None:
        """ Событие для кнопки btnBrush

            Аргументы:
                ** size: int - размер точки (овала)
                ** color: str - цвет точки (овала)

            Возвращает:
                None

            Побочный эффект:
                Очищаются все бинды и создаётся новый бинды на <ButtonRelease-1>, <B1-Motion> - отрисовка
                                                                                    последовательности точек (овалов)
        """

        for event in ('<ButtonRelease-1>', '<B1-Motion>'):
            self._root.bind(event, lambda e, c=self._canvas, s=size, clr=color:
                            self.__draw(e, c).point(size=s, color=clr))

    @__basic.reset
    def event_btnCreateLine(self,
                            *,
                            thickness: int = DEFAULT_THICKNESS,
                            color: str = DEFAULT_FIRST_COLOR) -> None:
        """ Событие для кнопки btnCreateLine

            Аргументы:
                ** thickness: int - жирность линии
                ** color: str - цвет линии

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 5 новых биндов <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                <KeyPress-Control_L>, <KeyRelease-Control_L> - отрисовка линии (отрезка)
        """

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>', '<KeyPress-Control_L>','<KeyRelease-Control_L>'):
            self._root.bind(event, lambda e, c=self._canvas, t=thickness, clr=color:
                            self.__draw(e, c).line(thickness=t, color=clr))

    @__basic.reset
    def event_btnCreateOval(self,
                            *,
                            thickness: int = DEFAULT_THICKNESS,
                            bgcolor: str = DEFAULT_SECOND_COLOR,
                            outcolor: str = DEFAULT_FIRST_COLOR) -> None:
        """ Событие для кнопки btnCreateOval

            Аргументы:
                ** thickness: int - жирность обводки эллипса
                ** bgcolor: str - цвет заливки эллипса
                ** outcolor: str - цвет обводки эллипса

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 5 новых биндов <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                        <KeyPress-Control_L>, <KeyRelease-Control_L> - отрисовка эллипса
        """

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>', '<KeyPress-Control_L>', '<KeyRelease-Control_L>'):
            self._root.bind(event, lambda e, c=self._canvas, t=thickness, bgclr=bgcolor, outclr=outcolor:
                            self.__draw(e, c).oval(thickness=t, bgcolor=bgclr, outcolor=outclr))

    @__basic.reset
    def event_btnCreateRectangle(self,
                                 *,
                                 thickness: int = DEFAULT_THICKNESS,
                                 bgcolor: str = DEFAULT_SECOND_COLOR,
                                 outcolor: str = DEFAULT_FIRST_COLOR) -> None:
        """ Событие для кнопки btnCreateOval

            Аргументы:
                ** thickness: int - жирность обводки прямоугольника
                ** bgcolor: str - цвет заливки прямоугольника
                ** outcolor: str - цвет обводки прямоугольника

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 5 новых биндов <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                    <KeyPress-Control_L>, <KeyRelease-Control_L> - отрисовка прямоугольника
        """

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>', '<KeyPress-Control_L>', '<KeyRelease-Control_L>'):
            self._root.bind(event, lambda e, c=self._canvas, t=thickness, bgclr=bgcolor, outclr=outcolor:
                            Draw(e, c).rectangle(thickness=t, bgcolor=bgclr, outcolor=outclr))

    def event_undo(self) -> None:
        """ Событие для бинда отмены действия (Ctrl-z)

            Возвращает:
                None

            Побочный эффект:
                Удаляет последний элемент из словаря с элементами
        """

        if self._canvas.obj_storage:
            key, value = self._canvas.obj_storage.popitem()
            self._canvas.delete(key)

    @__basic.reset
    def event_move(self, *, mouse_speed: int = DEFAULT_MOUSE_SPEED) -> None:
        """ Событие для кнопки btnMove

            Аргументы:
                ** mouse_speed: int - скорость передвижения объектов (скорость мыши) на слое (canvas'e)

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 3 новых бинла <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                    - движение объектов на canvas'e (слое)
        """

        for e in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>'):
            self._root.bind(e, lambda e, c=self._canvas, ms=mouse_speed: self.__draw(e, c).move(mouse_speed=ms))


# Создаём пример приложения
if __name__ == '__main__':

    # Тестируем все доктесты
    import doctest
    doctest.testmod()

    # Работа с иконкой
    from PIL import Image, ImageTk

    class App:
        """ App - пример приложение для проверки модуля """

        def __init__(self, root):
            ico = Image.open('visualist.png')
            ico.thumbnail((64, 64), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(ico)

            root.title('Visualist')
            root.wm_iconphoto(False, photo)

            frame_main = Frame(root)
            frame_main.pack()

            canvas = CustomCanvas(frame_main, width=DEFAULT_CANVAS_W, height=DEFAULT_CANVAS_H, bg=DEFAULT_CANVAS_BG)
            canvas.pack(side=RIGHT)

            events = Events(root, DEFAULT_USED_EVENTS, canvas)

            btnClear = Button(frame_main, text='*отчистить*', command=events.event_btnClear)
            btnClear.pack(side=TOP, pady=5)

            btnMove = Button(frame_main, text='*подвинуть*',
                             command=lambda ms=DEFAULT_MOUSE_SPEED: events.event_move(mouse_speed=ms))
            btnMove.pack(side=TOP, pady=5)

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
            root.bind('<Control-z>', lambda event: events.event_undo())
            root.bind('<Control-s>', lambda event: print(canvas.obj_storage))

    root = Tk(className='Visualist')
    App(root)
    root.mainloop()