# Импортированные модули
from ._draw import *
from core._defaults import *


class Events:
    """ Events - содержит все события для работы с окном

        Аргументы:
            * root: tkinter.Tk - главное окно
            * used_Events: Tuple[str] - список событий
            * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором происходит отрисовка

        Методы:
            * event_btnClear() -> None
            * event_btnBrush(*, size: int or float = DEFAULT_SIZE, color: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateLine(*, thickness: int or float = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateOval(*, thickness: int or float = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateRectangle(*, thickness: int or float = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreatePolygon(*, thickness: int or float = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateText(self) -> None
            * event_btnCreateVector(*, thickness: int or float = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None
            * event_btnCreateCoordinatePlane(*, thickness: int or float = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR):
            * event_undo() -> None
            * event_move(*, mouse_speed: int = DEFAULT_MOUSE_SPEED) -> None
            * event_btnFill(*, color: str = DEFAULT_CHANGE_COLOR) -> None
            * event_btnThickness(*, thickness: int or float = DEFAULT_THICKNESS) -> None
            * event_btnOutlineColor(*, color: str = DEFAULT_CHANGE_COLOR) -> None
            * event_btnQuickEraser(self) -> None
            * event_onCanvas(self) -> None
    """

    def __init__(self, root, used_events, canvas):
        self._root = root
        self._used_events = used_events
        self._canvas = canvas
        self.__draw = lambda event: Draw(root, event, canvas)

    @reset
    def event_btnClear(self):
        """ Событие для кнопки btnClear

            Возвращает:
                None

            Побочный эффект:
                Очистка canvas'a (слоя)
        """

        for obj in self._canvas.obj_storage.keys():
            self._canvas.delete(obj)
        self._canvas.itemconfig("photo", image="")
        self._canvas.obj_storage = {}
        self._canvas.modified_objs = []
        self._canvas.line_sequences = []
        self._canvas['background'] = 'white'

        __page = self._canvas.img
        __page["imgs"] = []
        __page["img_size"] = (800, 600)
        __page["ph"] = None
        __page["cr_img"] = None
        __page["curr_img"] = None

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
                            self.__draw(e).point(size=s, color=clr, debug_mode=dm))

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
    def event_btnCreateCoordinatePlane(self,
                                       *,
                                       thickness = DEFAULT_THICKNESS,
                                       color = DEFAULT_FIRST_COLOR):
        """ Событие для кнопки btnCreateCoordinatePlane

            Аргументы:
                ** thickness: int - жирность осей
                ** color: str - цвет осей

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 5 новых биндов <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                <KeyPress-Control_L>, <KeyRelease-Control_L> - отрисовка координатной плоскости
        """

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>', '<KeyPress-Control_L>','<KeyRelease-Control_L>'):
            self._root.bind(event, lambda e, t=thickness, clr=color:
                            self.__draw(e).coordinate_plane(thickness=t, color=clr))

    @reset
    def event_btnCreateVector(self,
                              *,
                              thickness = DEFAULT_THICKNESS,
                              color = DEFAULT_FIRST_COLOR):
        """ Событие для кнопки btnCreateVector

            Аргументы:
                ** thickness: int - жирность вектора
                ** color: str - цвет вектора

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 5 новых биндов <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                <KeyPress-Control_L>, <KeyRelease-Control_L> - отрисовка вектора
        """

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>', '<KeyPress-Control_L>','<KeyRelease-Control_L>'):
            self._root.bind(event, lambda e, t=thickness, clr=color:
                            self.__draw(e).line(thickness=t, color=clr, arrow=True))

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

    @reset
    def event_btnCreatePolygon(self,
                               *,
                               thickness = DEFAULT_THICKNESS,
                               bgcolor = DEFAULT_SECOND_COLOR,
                               outcolor = DEFAULT_FIRST_COLOR):
        """ Событие для кнопки btnCreatePolygon

            Аргументы:
                ** thickness: int - жирность обводки многоугольника
                ** bgcolor: str - цвет заливки многоугольника
                ** outcolor: str - цвет обводки многоугольника

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 5 новых биндов <ButtonPress-1>, <ButtonRelease-1>, <B1-Motion>,
                                                        <KeyPress-Control_L>, <KeyRelease-Control_L> - отрисовка многоугольника
                                                                                            (последовательности линий)

        """

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>', '<KeyPress-Control_L>', '<KeyRelease-Control_L>'):
            self._root.bind(event, lambda e, t=thickness, bgclr=bgcolor, outclr=outcolor:
                            self.__draw(e).polygon(thickness=t, bgcolor=bgclr, outcolor=outclr))

    @reset
    def event_btnCreateText(self):
        """ Событие для кнопки btnCreateText

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создёт ноый бинд <ButtonPress-1> - отрисовка текста
        """

        self._root.bind('<ButtonPress-1>', lambda e: self.__draw(e).text_creation())

    def event_undo(self, event):
        """ Событие для бинда отмены действия (Ctrl-z)

            Возвращает:
                None

            Побочный эффект:
                Создаёт новый бинд <Control-z> - отмена действия
        """

        self.__draw(event).undo()

    @reset
    def event_move(self):
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
            self._root.bind(event, lambda e:
                            self.__draw(e).move())

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

        self._root.bind('<B1-Motion>', lambda e: self.__draw(e).quick_eraser())

    def event_onCanvas(self):
        """ Событие для canvas'а

            Возвращает:
                None

            Побочный эффект:
                Создаёт новые бинды <Enter>, <Leave> для canvas - проверяет, находится курсор над canvas'ом (слоем) или нет
        """

        for event in ('<Enter>', '<Leave>'):
            self._canvas.bind(event, lambda e: self.__draw(e).on_canvas())

    @reset
    def event_btnThickness(self,
                           *,
                           thickness = DEFAULT_THICKNESS):
        """ Событие для кнопки btnThickness

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт новый бинд <ButtonPress-1> - изменение жирности обводки графического примитива
        """

        self._root.bind('<ButtonPress-1>', lambda e, t=thickness: self.__draw(e).thickness_objects(thickness=t))

    @reset
    def event_btnOutlineColor(self,
                              *,
                              color = DEFAULT_CHANGE_COLOR):
        """ Событие для кнопки btnOutlineColor

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт новый бинд <ButtonPress-1> - изменение цвета обводки графического примитива
        """

        self._root.bind('<ButtonPress-1>', lambda e, clr=color: self.__draw(e).outline_color_objects(color=clr))