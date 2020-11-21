# Импортированные модули
from ._draw import *
from ._defaults import *


class Events:
    """ Events - содержит все события для работы с окном

        Аргументы:
            * root: tkinter.Tk - главное окно
            * used_Events: Tuple[str] - список событий
            * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором происходит отрисовка

        Методы:
            * event_btnClear() -> None
            * event_btnBrush_Event(*, size: int = DEFAULT_SIZE, color: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateLine(*, thickness: int = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateOval(*, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateRectangle(*, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * event_undo() -> None
            * event_move(*, mouse_speed: int = DEFAULT_MOUSE_SPEED) -> None
            * event_btnEraser(self, *, size: int = DEFAULT_SIZE) -> None
            * event_btnFill(self, *, color: str = DEFAULT_CHANGE_COLOR) -> None
            * event_btnQuickEraser(self) -> None
    """

    def __init__(self, root, used_events, canvas):
        self._root = root
        self._used_events = used_events
        self._canvas = canvas
        self.__draw = lambda event: Draw(event, canvas)

    @reset
    def event_btnClear(self):
        """ Событие для кнопки btnClear

            Возвращает:
                None

            Побочный эффект:
                Очистка canvas'a (слоя)
        """

        self._canvas.obj_storage = {}
        self._canvas['background'] = 'white'
        self._canvas.delete('all')

    @reset
    def event_btnBrush(self,
                       *,
                       size = DEFAULT_BRUSH_SIZE,
                       color = DEFAULT_FIRST_COLOR,
                       debug_mode = False):
        """ Событие для кнопки btnBrush

            Аргументы:
                ** size: int - размер точки (линии)
                ** color: str - цвет точки (линии)
                ** debug_mode - режим отладчика

            Возвращает:
                None

            Побочный эффект:
                Очищаются все бинды и создаётся новый бинды на <ButtonRelease-1>, <B1-Motion> - отрисовка
                                                                                    последовательности линий (отрезков)
        """

        for event in ('<ButtonRelease-1>', '<B1-Motion>'):
            self._root.bind(event, lambda e, s=size, clr=color, dm=debug_mode:
                            self.__draw(e).point(size=s, color=clr, eraser=False, debug_mode=dm))

    @reset
    def event_btnCreateLine(self,
                            *,
                            thickness = DEFAULT_THICKNESS,
                            color = DEFAULT_FIRST_COLOR):
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
            self._root.bind(event, lambda e, t=thickness, clr=color:
                            self.__draw(e).line(thickness=t, color=clr))

    @reset
    def event_btnCreateOval(self,
                            *,
                            thickness = DEFAULT_THICKNESS,
                            bgcolor = DEFAULT_SECOND_COLOR,
                            outcolor = DEFAULT_FIRST_COLOR):
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
            self._root.bind(event, lambda e, t=thickness, bgclr=bgcolor, outclr=outcolor:
                            self.__draw(e).oval(thickness=t, bgcolor=bgclr, outcolor=outclr))

    @reset
    def event_btnCreateRectangle(self,
                                 *,
                                 thickness = DEFAULT_THICKNESS,
                                 bgcolor = DEFAULT_SECOND_COLOR,
                                 outcolor = DEFAULT_FIRST_COLOR):
        """ Событие для кнопки btnCreateRectangle

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
            self._root.bind(event, lambda e, t=thickness, bgclr=bgcolor, outclr=outcolor:
                            self.__draw(e).rectangle(thickness=t, bgcolor=bgclr, outcolor=outclr))

    def event_undo(self):
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
    def event_move(self,
                   *,
                   mouse_speed = DEFAULT_MOUSE_SPEED):
        """ Событие для кнопки btnMove

            Аргументы:
                ** mouse_speed: int - скорость передвижения объектов (скорость мыши) на слое (canvas'e)

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 3 новых бинда <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                    - движение объектов на canvas'e (слое)
        """

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>'):
            self._root.bind(event, lambda e, ms=mouse_speed:
                            self.__draw(e).move(mouse_speed=ms))

    @reset
    def event_btnEraser(self,
                        *,
                        size = DEFAULT_ERASER_SIZE):
        """ Событе для кнопки btnEraser

            Аргументы:
                ** size: int - размер точки (линии)

            Возвращает:
                None

            Побочный эффект:
                Очищаются все бинды и создаётся новые бинды на <ButtonRelease-1>, <B1-Motion> - отрисовка
                                                                                    последовательности линий (отрезков)
        """

        for event in ('<ButtonRelease-1>', '<B1-Motion>'):
            self._root.bind(event, lambda e, s=size, clr=self._canvas['background']:
                            self.__draw(e).point(size=s, color=clr, eraser=True, debug_mode=False))

    @reset
    def event_btnFill(self,
                      *,
                      color = DEFAULT_CHANGE_COLOR):
        """ Событие для кнопки btnFill

            Аргументы:
                ** color: str - цвет в который будет перекрашен объект

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт новый бинд <ButtonPress-1> - заливка графических примитивов
        """

        self._root.bind('<ButtonPress-1>', lambda e, c=color:
                        self.__draw(e).fill_objects(color=c))

    @reset
    def event_btnQuickEraser(self):
        """ Событие для кнопки btnQuickEraser

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт новый бинд <ButtonPress-1> - удаляет графический примитив с canvas'а (слоя)
        """

        self._root.bind('<ButtonPress-1>', lambda e: self.__draw(e).quick_eraser())