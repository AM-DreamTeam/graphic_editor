# Импортированные модули
from ._draw import *
from typing import Tuple    # TODO: сделать pyi-file
from tkinter import Tk


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

    @reset
    def event_btnClear(self) -> None:
        """ Событие для кнопки btnClear

            Возвращает:
                None

            Побочный эффект:
                Очистка canvas'a (слоя)
        """

        self._canvas.obj_storage = {}
        self._canvas.delete('all')

    @reset
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

    @reset
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

    @reset
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

    @reset
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

    @reset
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