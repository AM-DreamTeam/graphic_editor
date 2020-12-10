""" Новые настраиваемые объекты """


# Импортированные модулей
from core.image_lib._image_processing import Img
from core.graphic_lib._events import Events
from core._defaults import *
from tkinter import *
from tkinter import ttk


class CustomCanvas(Canvas):
    """ CustomCanvas - для того, чтобы не портить canvas из моудля tkinter создадим класс с расширенными полями и методами

        Атрибуты:
            * old_point: None or Tuple[int] - временное хранилище прошлых координат точки
            * obj_oval: None or Oval - временное хранилище эллипса
            * obj_line: None or Line - временное хранилище прямой (отрезка)
            * obj_rectangle: None or Rectangle - временное хранилище прямоугольника
            * obj_horizontal_axis: None or Line - временное хранилище для горизонтальной оси
            * obj_vertical_axis: None or Line - временное хранилище для вертиальной оси
            * line_sequences: list - хранение последовательности линий
            * obj_storage: dict - хранилище графических примитивов на слое (canvas'e)
            * start_point: None or Tuple[int, int] - хранит начальную точку для многоугольников
            * modified_objs = [] - хранит список тэгов изменённых объектов
            * obj_tag: None or str - временное хранилище tag'ов объектов, на которые нажимает пользователь
            * hover: bool - хранит логическое значение, находится ли курсор над canvas'ом или нет
            * img: dict - словарь для хранения информации о холстах
            * undo: dict - список для хранения метод с каким из двух типов объектов мы работали (с графическими примитивами или с фото)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """ ============= graphic_lib ============ """

        self.old_point = None

        self.obj_oval = None
        self.obj_line = None
        self.obj_rectangle = None
        self.obj_horizontal_axis = None
        self.obj_vertical_axis = None

        self.line_sequences = []
        self.obj_storage = {'canvas': {'color': [DEFAULT_CANVAS_BG]}}
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
                     "scroll_speed": 10.,                                   # скорость прокрутки скроллов
                     "curr_img": None                                       # временное хранилище фотографии
                    }
        self.undo = []


class NotebookTabs(ttk.Notebook):

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None
        self._closed_tabs = []

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Вызывается при нажатии кнопки закрытия"""
        if len(self.tabs()) > 1:
            element = self.identify(event.x, event.y)

            if "close" in element:
                index = self.index("@%d,%d" % (event.x, event.y))
                self.state(['pressed'])
                self._active = index

    def on_close_release(self, event):
        """Вызывается, когда кнопка закрытия отпускается"""
        if len(self.tabs()) > 1:
            if not self.instate(['pressed']):
                return

            __element = self.identify(event.x, event.y)
            __index = self.index("@%d,%d" % (event.x, event.y))

            if "close" in __element and self._active == __index:
                self._closed_tabs.append(self.tabs()[__index])
                self.hide(__index)
                # self.event_generate("<<NotebookTabClosed>>")

            self.state(["!pressed"])
            self._active = None

    def reestablish_tab(self):
        """
        Восстанавливает последнюю закрытую вкладку
        """
        if self._closed_tabs:
            __index = self._closed_tabs.pop()
            self.add(__index)
            self.select(__index)

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                             ("active", "pressed", "!disabled", "img_closepressed"),
                             ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])


class CustomNotebook(NotebookTabs):
    """ CustomNotebook - расширенный, настраиваемый Notebook из модуля tkinter, чтобы не пачкать уже существующий

        Аргументы:
            * root: tkinter.Tk - главное окно

        Методы:
            * create_new_canvas(self) -> None
            * select_curr_tab(self, event: tkinter.Tk) -> None
            * undo(self, event: tkinter.Tk) -> None
    """

    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)

        # фрейм, в который мы складывает холст и скроллы
        __frame = Frame(self)
        self.add(__frame, text='Холст 1')

        __scroll_x = Scrollbar(__frame, orient=HORIZONTAL)
        __scroll_y = Scrollbar(__frame, orient=VERTICAL)

        self._canvas = CustomCanvas(__frame,
                                    width=DEFAULT_CANVAS_W,
                                    height=DEFAULT_CANVAS_H,
                                    bg=DEFAULT_CANVAS_BG,
                                    xscrollcommand=__scroll_x.set,
                                    yscrollcommand=__scroll_y.set
                                    )

        __scroll_x.config(command=self._canvas.xview)
        __scroll_y.config(command=self._canvas.yview)

        __scale_label = Label(__frame, text="Масштаб: 100%")

        # упаковываем все и настраиваем
        self._canvas.grid(column=0, row=0, sticky="nswe")
        __scroll_x.grid(column=0, row=1, sticky="we")
        __scroll_y.grid(column=1, row=0, sticky="ns")
        __scale_label.grid(column=0, row=2, sticky="e")
        __frame.rowconfigure(0, weight=1)
        __frame.columnconfigure(0, weight=1)
        self._canvas.configure(yscrollincrement='11', xscrollincrement='11')

        self._count = 1
        self._canvas.img["id"] = self._count

        self.root = root
        self._canvases = [self._canvas]

        # активация ядер
        self.image_processing = Img(self.root, self._canvas)
        self.events = Events(self.root, DEFAULT_USED_EVENTS, self._canvas)
        self.events.event_onCanvas()

        # привязываем события к холсту
        self._canvas.bind("<Button 3>", lambda event: self.image_processing.grab(event))
        self._canvas.bind("<B3-Motion>", lambda event: self.image_processing.drag(event))
        self._canvas.bind("<Control-MouseWheel>", lambda event: [
                                                                 self.image_processing.zoom(event),
                                                                 __scale_label.config(text=f"Масштаб: {round(self._canvas.img['scale'] * 100, 2)}%")
                                                                ]
                          )
        self._canvas.bind("<Control-Button-4>", lambda event: self.image_processing.zoom_in(event))
        self._canvas.bind("<Control-Button-5>", lambda event: self.image_processing.zoom_off(event))

        self.root.bind('<Control-s>', lambda event: print(self._canvas.modified_objs, self._canvas.obj_storage)) # TODO: Избавится от этого, нужно лишь для debug'a


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

        self._canvas = CustomCanvas(__frame,
                                    width=DEFAULT_CANVAS_W,
                                    height=DEFAULT_CANVAS_H,
                                    bg=DEFAULT_CANVAS_BG,
                                    xscrollcommand=__scroll_x.set,
                                    yscrollcommand=__scroll_y.set
                                    )

        __scroll_x.config(command=self._canvas.xview)
        __scroll_y.config(command=self._canvas.yview)

        __scale_label = Label(__frame, text="Масштаб: 100%")

        self._canvas.grid(column=0, row=0, sticky="nswe")
        __scroll_x.grid(column=0, row=1, sticky="we")
        __scroll_y.grid(column=1, row=0, sticky="ns")
        __scale_label.grid(column=0, row=2, sticky="e")
        __frame.rowconfigure(0, weight=1)
        __frame.columnconfigure(0, weight=1)
        self._canvas.configure(yscrollincrement='10.', xscrollincrement='10.')

        # активация ядер
        self.image_processing = Img(self.root, self._canvas)
        self.events = Events(self.root, DEFAULT_USED_EVENTS, self._canvas)
        self.events.event_onCanvas()

        self._canvas.bind("<Button 3>", lambda event: self.image_processing.grab(event))
        self._canvas.bind("<B3-Motion>", lambda event: self.image_processing.drag(event))
        self._canvas.bind("<Control-MouseWheel>", lambda event: [
                                                                 self.image_processing.zoom(event),
                                                                 __scale_label.config(text=f"Масштаб: {round(self._canvas.img['scale'] * 100, 2)}%")
                                                                ]
                          )
        self._canvas.bind("<Control-Button-4>", lambda event: self.image_processing.zoom_in(event))
        self._canvas.bind("<Control-Button-5>", lambda event: self.image_processing.zoom_off(event))


        self.root.bind('<Control-s>', lambda event: print(self._canvas.modified_objs, self._canvas.obj_storage))
        self._canvas.img["id"] = self._count
        self._canvases.append(self._canvas)
        self.select(self.tabs()[-1])

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

            self._canvas = self._canvases[__id-1]

            self.image_processing = Img(self.root, self._canvas)
            self.events = Events(self.root, DEFAULT_USED_EVENTS, self._canvas)
            self.root.bind('<Control-s>', lambda e: print(self._canvas.modified_objs, self._canvas.obj_storage))
        except TclError:
            pass

    def undo(self, event=None):
        """ Событие отмены действия

            Аргументы:
                * event: tkinter.Event - событие для отмены действия

            Возвращает:
                None

            Побочный эффект:
                Обновляет графическое ядро и ядро для работы с фотографиями
        """
        print("undo")
        __acts = self._canvas.undo
        if __acts:
            __last_act = self._canvas.undo.pop()
            if __last_act == "image":
                self.image_processing.return_image()
            elif __last_act == "graphic":
                self.events.event_undo(event)
