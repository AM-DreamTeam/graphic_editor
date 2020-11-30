""" Новые настраиваемые объекты """


# Импортированные модулей
from image_lib._image_processing import Img
from graphic_lib._events import Events
from tkinter.ttk import Notebook
from image_lib._defaults import *
from tkinter import *


class CustomCanvas(Canvas):
    """ CustomCanvas(Canvas) - для того, чтобы не портить canvas из моудля tkinter создадим класс с расширенными полями
    и методами

        Поля:
            * old_point: None or Tuple[int] - временное хранилище прошлых координат точки
            * obj_oval: None or Oval - временное хранилище эллипса
            * obj_line: None or Line - временное хранилище прямой (отрезка)
            * obj_rectangle: None or Rectangle - временное хранилище прямоугольника
            * line_sequences: list - хранение последовательности линий
            * obj_storage: dict - хранилище графических примитивов на слое (canvas'e)
            * start_point: None or Tuple[int, int] - хранит начальную точку для многоугольников
            * obj_tag: None or str - временное хранилище tag'ов объектов, на которые нажимает пользователь
            * hover: bool - хранит логическое значение, находится ли курсор над canvas'ом или нет
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.old_point = None

        self.obj_oval = None
        self.obj_line = None
        self.obj_rectangle = None

        self.line_sequences = []
        self.line_storage = []
        self.obj_storage = {}
        self.start_point = None

        self.modified_objs = []
        self.obj_tag = None

        self.hover = False

        self.img = {
             "id": None,  # номер холста
             "imgs": [],  # история изображений
             "cr_img": None,  # объект crete_image, с помощью котого изменяяем картинку
             "img_size": (DEFAULT_CANVAS_W, DEFAULT_CANVAS_H),  # размер текущей картинки
             "ph": None,  # объект ImageTk, который лежит в create_image
             "scale": 1.0,  # коэффициент масштабирования
             "scale_size": (DEFAULT_CANVAS_W, DEFAULT_CANVAS_H),  # размеры изображения при масштабировании
             "scroll_speed": 11.  # скорость прокрутки скроллов
             }


class CustomNotebook(Notebook):
    def __init__(self, root, **kw):
        super().__init__(**kw)
        self.root = root

        # фрейм, в который мы складывает холст и скроллы
        frame = Frame(self)
        self.add(frame, text='Холст 1')

        scroll_x = Scrollbar(frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame, orient=VERTICAL)

        canvas = CustomCanvas(frame,
                              width=DEFAULT_CANVAS_W,
                              height=DEFAULT_CANVAS_H,
                              bg=DEFAULT_CANVAS_BG,
                              xscrollcommand=scroll_x.set,
                              yscrollcommand=scroll_y.set
                              )

        scroll_x.config(command=canvas.xview)
        scroll_y.config(command=canvas.yview)

        # упаковываем все и настраиваем
        canvas.grid(column=0, row=0, sticky="nswe")
        scroll_x.grid(column=0, row=1, sticky="we")
        scroll_y.grid(column=1, row=0, sticky="ns")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        canvas.configure(yscrollincrement='11', xscrollincrement='11')

        # привязываем события к холсту
        # canvas.bind("<Button 3>", lambda event: self.image_processing.grab(event))
        # canvas.bind("<B3-Motion>", lambda event: self.image_processing.drag(event))
        # canvas.bind("<MouseWheel>", lambda event: self.image_processing.zoom(event))

        self.count = 1
        canvas.img["id"] = self.count
        self.image_processing = Img(canvas)
        self.canvases = [canvas]


        self.root.bind('<Control-x>', quit)
        self.root.bind('<Control-s>', lambda event: print(canvas.modified_objs, canvas.obj_storage))
        self.events = Events(root, DEFAULT_USED_EVENTS, canvas)
        self.events.event_onCanvas()
        self.events.event_undo()
        self.root = root

    def create_new_canvas(self):
        """
        Создает новую вкладку на notebook и размещает на нем новый холст
        """
        self.count += 1

        frame = Frame(self)
        self.add(frame, text=f"Холст {self.count}")

        scroll_x = Scrollbar(frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame, orient=VERTICAL)

        canvas = CustomCanvas(frame,
                              width=DEFAULT_CANVAS_W,
                              height=DEFAULT_CANVAS_H,
                              bg=DEFAULT_CANVAS_BG,
                              xscrollcommand=scroll_x.set,
                              yscrollcommand=scroll_y.set
                              )

        scroll_x.config(command=canvas.xview)
        scroll_y.config(command=canvas.yview)

        canvas.grid(column=0, row=0, sticky="nswe")
        scroll_x.grid(column=0, row=1, sticky="we")
        scroll_y.grid(column=1, row=0, sticky="ns")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        canvas.configure(yscrollincrement='11', xscrollincrement='11')

        canvas.bind("<Button 3>", lambda event: self.image_processing.grab(event))
        canvas.bind("<B3-Motion>", lambda event: self.image_processing.drag(event))
        canvas.bind("<MouseWheel>", lambda event: self.image_processing.zoom(event))


        self.root.bind('<Control-x>', quit)
        self.root.bind('<Control-s>', lambda event: print(canvas.modified_objs, canvas.obj_storage))
        self.events = Events(self.root, DEFAULT_USED_EVENTS, canvas)
        self.events.event_onCanvas()
        self.events.event_undo()

        canvas.img["id"] = self.count
        self.select(self.count-1)
        self.canvases.append(canvas)

    def select_curr_tab(self, event):

        selected_canvas = event.widget.select()
        __id = int(event.widget.tab(selected_canvas, "text")[-1])

        __canvas = self.canvases[__id-1]

        self.image_processing = Img(__canvas)
        self.events = Events(self.root, DEFAULT_USED_EVENTS, __canvas)
        self.events.event_undo()
