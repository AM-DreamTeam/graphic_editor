""" Новые настраиваемые объекты """


# Импортированные модулей
from core._custom_notebook import *
from core.image_lib._image_processing import Img
from core.graphic_lib._events import Events
from core._defaults import *
from tkinter import *


class CustomCanvas(Canvas):
    """ CustomCanvas - для того, чтобы не портить canvas из моудля tkinter создадим класс с расширенными полями и методами

        Атрибуты:
            * old_point: None or Tuple[int] - временное хранилище прошлых координат точки
            * obj_oval: None or Oval - временное хранилище эллипса
            * obj_line: None or Line - временное хранилище прямой (отрезка)
            * obj_rectangle: None or Rectangle - временное хранилище прямоугольника
            * line_sequences: list - хранение последовательности линий
            * obj_storage: dict - хранилище графических примитивов на слое (canvas'e)
            * start_point: None or Tuple[int, int] - хранит начальную точку для многоугольников
            * modified_objs = [] - хранит список тэгов изменённых объектов
            * obj_tag: None or str - временное хранилище tag'ов объектов, на которые нажимает пользователь
            * hover: bool - хранит логическое значение, находится ли курсор над canvas'ом или нет
            * img: dict - словарь для хранения информации о холстах
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """ ============= graphic_lib ============ """

        self.old_point = None

        self.obj_oval = None
        self.obj_line = None
        self.obj_rectangle = None

        self.line_sequences = []
        self.obj_storage = {}
        self.start_point = None

        self.modified_objs = []
        self.obj_tag = None

        self.hover = False

        """ ============= image_lib ============ """

        self.img = {
                     "id": None,                                            # номер холста
                     "imgs": [],                                            # история изображений
                     "cr_img": None,                                        # объект crete_image, с помощью котого изменяяем картинку
                     "img_size": (DEFAULT_CANVAS_W, DEFAULT_CANVAS_H),      # размер текущей картинки
                     "ph": None,                                            # объект ImageTk, который лежит в create_image
                     "scale": 1.0,                                          # коэффициент масштабирования
                     "scale_size": (DEFAULT_CANVAS_W, DEFAULT_CANVAS_H),    # размеры изображения при масштабировании
                     "scroll_speed": 10.                                    # скорость прокрутки скроллов
                }

        self.drawQ = True                                                  # было ли что-то нарисовано?


class CustomNotebook(NotebookTabs):
    """ CustomNotebook - расширенный, настраиваемый Notebook из модуля tkinter, чтобы не пачкать уже существующий

        Аргументы:
            * root: tkinter.Tk - главное окно

        Методы:
            * create_new_canvas(self) -> None
            * select_curr_tab(self, event) -> None
    """

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        # фрейм, в который мы складывает холст и скроллы
        __frame = Frame(self)
        self.add(__frame, text='Холст 1')

        __scroll_x = Scrollbar(__frame, orient=HORIZONTAL)
        __scroll_y = Scrollbar(__frame, orient=VERTICAL)

        __canvas = CustomCanvas(__frame,
                                width=DEFAULT_CANVAS_W,
                                height=DEFAULT_CANVAS_H,
                                bg=DEFAULT_CANVAS_BG,
                                xscrollcommand=__scroll_x.set,
                                yscrollcommand=__scroll_y.set
                                )

        __scroll_x.config(command=__canvas.xview)
        __scroll_y.config(command=__canvas.yview)

        # упаковываем все и настраиваем
        __canvas.grid(column=0, row=0, sticky="nswe")
        __scroll_x.grid(column=0, row=1, sticky="we")
        __scroll_y.grid(column=1, row=0, sticky="ns")
        __frame.rowconfigure(0, weight=1)
        __frame.columnconfigure(0, weight=1)
        __canvas.configure(yscrollincrement='11', xscrollincrement='11')

        self._count = 1
        __canvas.img["id"] = self._count
        self.image_processing = Img(__canvas)

        self.root = root
        self._canvases = [__canvas]

        # привязываем события к холсту
        __canvas.bind("<Button 3>", lambda event: self.image_processing.grab(event))
        __canvas.bind("<B3-Motion>", lambda event: self.image_processing.drag(event))
        __canvas.bind("<MouseWheel>", lambda event: self.image_processing.zoom(event))

        self.root.bind('<Control-s>', lambda event: print(__canvas.modified_objs, __canvas.obj_storage)) # TODO: Избавится от этого, нужно лишь для debug'a

        self.events = Events(self.root, DEFAULT_USED_EVENTS, __canvas)
        self.events.event_onCanvas()
        self.events.event_undo()

    def create_new_canvas(self):
        """ Создает новую вкладку на notebook и размещает на нем новый холст

            Возвращает:
                None
        """

        self._count += 1

        __frame = Frame(self)
        self.add(__frame, text=f"Холст {self._count}")

        __scroll_x = Scrollbar(__frame, orient=HORIZONTAL)
        __scroll_y = Scrollbar(__frame, orient=VERTICAL)

        __canvas = CustomCanvas(__frame,
                                width=DEFAULT_CANVAS_W,
                                height=DEFAULT_CANVAS_H,
                                bg=DEFAULT_CANVAS_BG,
                                xscrollcommand=__scroll_x.set,
                                yscrollcommand=__scroll_y.set
                                )

        __scroll_x.config(command=__canvas.xview)
        __scroll_y.config(command=__canvas.yview)

        __canvas.grid(column=0, row=0, sticky="nswe")
        __scroll_x.grid(column=0, row=1, sticky="we")
        __scroll_y.grid(column=1, row=0, sticky="ns")
        __frame.rowconfigure(0, weight=1)
        __frame.columnconfigure(0, weight=1)
        __canvas.configure(yscrollincrement='10.', xscrollincrement='10.')

        __canvas.bind("<Button 3>", lambda event: self.image_processing.grab(event))
        __canvas.bind("<B3-Motion>", lambda event: self.image_processing.drag(event))
        __canvas.bind("<MouseWheel>", lambda event: self.image_processing.zoom(event))

        self.root.bind('<Control-x>', quit)
        self.root.bind('<Control-s>', lambda event: print(__canvas.modified_objs, __canvas.obj_storage))     # TODO: Избавится от этого, нужно лишь для debug'a
        self.events = Events(self.root, DEFAULT_USED_EVENTS, __canvas)
        self.events.event_onCanvas()
        self.events.event_undo()

        __canvas.img["id"] = self._count
        self.select(self.tabs()[-1])
        self._canvases.append(__canvas)

    def select_curr_tab(self, event):
        """ Событие при переходе на новую вкладку

            Аргументы:
                event: tkinter.Event - событие, по которому считывается текущая вкладка

            Возвращает:
                None

            Побочный эффект:
                Обновляет графическое ядро и ядро для работы с фотографиями
        """
        try:
            __selected_canvas = event.widget.select()
            __id = int(event.widget.tab(__selected_canvas, "text")[-1])

            __canvas = self._canvases[__id-1]

            self.image_processing = Img(__canvas)
            self.events = Events(self.root, DEFAULT_USED_EVENTS, __canvas)
            self.events.event_undo()
        except _tkinter.TclError:
            pass

