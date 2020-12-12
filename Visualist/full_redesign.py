from tkinter import *
from tkinter import Menu
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import tkinter.colorchooser
from core import _tool_tip
from core import core
from tkinter import messagebox


class App(Tk, ThemedStyle):
    def __init__(self):
        super().__init__()
        self.init_main()

        # лого
        ico = Image.open('images/visualist.png')
        ico.thumbnail((64, 64), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)

        ThemedStyle(self, theme='black')

    def reset_scales(self, _=None):
        """
            Сбрасывает значения Scale до 100 при смене вкладки
        """
        self.filter_2_percent.set(100)
        self.r_scale_box.set(100)
        self.g_scale_box.set(100)
        self.b_scale_box.set(100)

    def close_window(self):
        """
        обработка закрытия окна
        """
        x = lambda: self.notebook.save_q()
        if not x():
            if messagebox.askyesno("Выход", "У Вас есть несохраненные данные. Вы действительно хотите выйти?"):
                self.destroy()
        else:
            self.destroy()

    def init_main(self):
        """ Содержит в себе инициальзацию основного окна"""

        # параметры стилизации
        self.dir = 'gifblack'
        self.font = "courier"
        self.format = 'gif'
        self.font_par = ("Comic Sans MS", 15, "bold")

        # вспомогательные функции
        def image_resize(size: tuple, pic: str):
            """ Изменяет размер иконки

            Аргументы:
                size: объект типа tuple содеражщий высоту и ширину выводимого изображения
                pic: директория изображения

            Возвращает:
                изображение класса ImageTk
            """
            return ImageTk.PhotoImage(Image.open(pic).resize(size))

        self.color_code = ((0.0, 0.0, 0.0), 'black')

        def choose_color():
            self.color_code = tkinter.colorchooser.askcolor(title="Цвета")
            self.btn_color.config(bg=self.color_code[1])

        def slider_filter2(value):
            """ Изменяет значение индикатора слайдера

                Аргументы:
                    value: текущее значение(положение) слайдера

                По аналогии с slider_filter_r, slider_filter_g, slider_filter_b, slider_thickness
            """
            self.value_label.config(text=round(float(value)))

        def slider_filter_r(value):
            self.r_scale_value.config(text=f'{round(float(value))} %')

        def slider_filter_g(value):
            self.g_scale_value.config(text=f'{round(float(value))} %')

        def slider_filter_b(value):
            self.b_scale_value.config(text=f'{round(float(value))} %')

        self.thickness = 5

        def slider_thickness(value):
            self.thickness_value.config(text=round(float(value)))
            self.thickness = round(float(value))

        # создание холста
        self.notebook = core.CustomNotebook(self)
        self.notebook.grid(row=2, column=0, rowspan=2, sticky="nsew")

        # меню
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=-2)
        self.filemenu.add_command(label="Открыть...", command=lambda: self.notebook.image_processing.set_image())
        self.filemenu.add_command(label="Сохранить...", command=lambda: self.notebook.save_canvas())
        self.filemenu.add_command(label="Настройки",)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Выход", command=self.close_window)
        self.menubar.add_cascade(label="Файл", menu=self.filemenu)
        self.menubar.add_command(label='info', command=lambda: self.notebook.image_processing.get_info())  # TODO: убрать
        self.config(menu=self.menubar)

        self.notebook.bind("<<NotebookTabChanged>>", self.notebook.select_curr_tab)
        self.bind('<Control-z>', lambda e: self.notebook.undo(e))
        self.bind('<Control-x>', quit)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # изменине окна
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

        # GUI виджеты
        self.nb = ttk.Notebook(self)
        self.toolbar_1 = ttk.Frame(self.nb)
        self.toolbar_2 = ttk.Frame(self.nb)
        self.toolbar_3 = ttk.Frame(self.nb)
        self.nb.add(self.toolbar_1, text='Инструменты')
        self.nb.add(self.toolbar_2, text='Фильтры')

        self.main_toolbar = ttk.Frame(self)

        self.main_toolbar.grid(row=1, column=0, sticky="WE")
        self.nb.grid(row=0, column=0, sticky="WE")

            # панель
        self.im_add_list = image_resize((30, 30), f"images/{self.dir}/add_list.{self.format}")
        self.btn_add_list = ttk.Button(self.main_toolbar,
                                       text="Добавить холст",
                                       image=self.im_add_list,
                                       compound=LEFT,
                                       command=self.notebook.create_new_canvas)

        self.im_back_list = image_resize((30, 30), f"images/{self.dir}/back_list.{self.format}")
        self.btn_back_list = ttk.Button(self.main_toolbar,
                                        text="Вернуть холст",
                                        image=self.im_back_list,
                                        compound=LEFT,
                                        command=lambda: self.notebook.reestablish_tab())

        self.im_undo = image_resize((20, 20), f"images/{self.dir}/undo.{self.format}")
        self.btn_undo = ttk.Button(self.main_toolbar,
                                   image=self.im_undo,
                                   command=lambda: self.notebook.undo())
        _tool_tip.ToolTip(self.btn_undo, "Вернуть")

        self.im_replace = image_resize((20, 20), f"images/{self.dir}/replace.{self.format}")
        self.btn_replace = ttk.Button(self.main_toolbar,
                                      image=self.im_replace,
                                      command=lambda: [self.notebook.events.event_move(),
                                                       self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_replace, "Перенести")

        self.im_clear = image_resize((20, 20), f"images/{self.dir}/delete.{self.format}")
        self.btn_clear = ttk.Button(self.main_toolbar,
                                    image=self.im_clear,
                                    command=lambda: [self.notebook.events.event_btnClear(),
                                                     self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_clear, "Очистить холст")

        self.sun = image_resize((20, 20), f"images/{self.dir}/sun.{self.format}")
        self.moon = image_resize((20, 20), f"images/{self.dir}/moon.{self.format}")

            # страница 1

        self.im_brush = image_resize((30, 30), f"images/{self.dir}/brush.{self.format}")
        self.btn_brush = ttk.Button(self.toolbar_1,
                                    image=self.im_brush,
                                    command=lambda: [self.notebook.events.event_btnBrush(size=self.thickness,
                                                                                         color=self.color_code[1],
                                                                                         debug_mode=False),
                                                     self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_brush, "Кисточка")

        self.im_fill = image_resize((30, 30), f"images/{self.dir}/fill.{self.format}")
        self.btn_fill = ttk.Button(self.toolbar_1,
                                   image=self.im_fill,
                                   command=lambda: [self.notebook.events.event_btnFill(color=self.color_code[1]),
                                                    self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_fill, "Заливка")

        self.im_text = image_resize((30, 30), f"images/{self.dir}/text.{self.format}")
        self.btn_text = ttk.Button(self.toolbar_1,
                                   image=self.im_text,
                                   command=lambda: [self.notebook.events.event_btnCreateText(),
                                                    self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_text, "Текст")

        self.im_eraser = image_resize((30, 30), f"images/{self.dir}/eraser.{self.format}")
        self.btn_eraser = ttk.Button(self.toolbar_1,
                                     image=self.im_eraser,
                                     command=lambda: [self.notebook.events.event_btnQuickEraser(),
                                                      self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_eraser, "Ластик")

        self.im_color = image_resize((85, 85), f"images/{self.dir}/color.{self.format}")
        self.btn_colorchoice = ttk.Button(self.toolbar_1,
                                          image=self.im_color,
                                          command=lambda: [choose_color(),
                                                           self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_colorchoice, "Выбор цвета")

        self.color_frame = ttk.Frame(self.toolbar_1)
        self.btn_color = Button(self.color_frame, bg=self.color_code[1])
        _tool_tip.ToolTip(self.btn_color, "Текущий цвет")

        self.thickness_labelframe = ttk.Labelframe(self.toolbar_1, text="Толщина")

        self.pic_thickness_1 = image_resize((100, 5), f"images/{self.dir}/lineth4.{self.format}")
        self.btn_thickness_1 = ttk.Button(self.thickness_labelframe,
                                          image=self.pic_thickness_1,
                                          command=lambda: [self.notebook.events.event_btnThickness(thickness=5),
                                                           self.thickness_value.config(text=5),
                                                           self.thickness_scale.set(5)])
        _tool_tip.ToolTip(self.btn_thickness_1, "Толщина - 5")

        self.pic_thickness_2 = image_resize((100, 7), f"images/{self.dir}/lineth4.{self.format}")
        self.btn_thickness_2 = ttk.Button(self.thickness_labelframe,
                                          image=self.pic_thickness_2,
                                          command=lambda: [self.notebook.events.event_btnThickness(thickness=10),
                                                           self.thickness_value.config(text=10),
                                                           self.thickness_scale.set(10)])
        _tool_tip.ToolTip(self.btn_thickness_2, "Толщина - 10")

        self.pic_thickness_3 = image_resize((100, 9), f"images/{self.dir}/lineth4.{self.format}")
        self.btn_thickness_3 = ttk.Button(self.thickness_labelframe,
                                          image=self.pic_thickness_3,
                                          command=lambda: [self.notebook.events.event_btnThickness(thickness=15),
                                                           self.thickness_value.config(text=15),
                                                           self.thickness_scale.set(15)])
        _tool_tip.ToolTip(self.btn_thickness_3, "Толщина - 15")

        self.pic_thickness_4 = image_resize((100, 11), f"images/{self.dir}/lineth4.{self.format}")
        self.btn_thickness_4 = ttk.Button(self.thickness_labelframe,
                                          image=self.pic_thickness_4,
                                          command=lambda: [self.notebook.events.event_btnThickness(thickness=20),
                                                           self.thickness_value.config(text=20),
                                                           self.thickness_scale.set(20)])
        _tool_tip.ToolTip(self.btn_thickness_4, "Толщина - 20")

        self.thickness_value = ttk.Label(self.thickness_labelframe,
                                         text=self.thickness,
                                         foreground='black',
                                         width=3,
                                         anchor=N,
                                         font=self.font_par)
        self.thickness_scale = ttk.Scale(self.thickness_labelframe,
                                         orient=VERTICAL,
                                         length=50,
                                         from_=1,
                                         to=20,
                                         command=slider_thickness)

        self.figure_labelframe = ttk.Labelframe(self.toolbar_1, text="Фигуры")

        self.pic_rectangle = image_resize((25, 20), f"images/{self.dir}/rectangle.{self.format}")
        self.btn_rectangle = ttk.Button(self.figure_labelframe,
                                        image=self.pic_rectangle,
                                        command=lambda
                                        bgclr=core.DEFAULT_SECOND_COLOR:
                                        [self.notebook.events.event_btnCreateRectangle(thickness=self.thickness,
                                                                                       bgcolor=bgclr,
                                                                                       outcolor=self.color_code[1]),
                                         self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_rectangle, "Прямоугольник")

        self.pic_polygon = image_resize((25, 20), f"images/{self.dir}/polygon.{self.format}")
        self.btn_polygon = ttk.Button(self.figure_labelframe,
                                      image=self.pic_polygon,
                                      command=lambda bgclr=core.DEFAULT_SECOND_COLOR:
                                      [self.notebook.events.event_btnCreatePolygon(thickness=self.thickness,
                                                                                   bgcolor=bgclr,
                                                                                   outcolor=self.color_code[1]),
                                       self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_polygon, "Многоугольник")

        self.pic_ellipsis = image_resize((25, 20), f"images/{self.dir}/ellipsis.{self.format}")
        self.btn_ellipsis = ttk.Button(self.figure_labelframe,
                                       image=self.pic_ellipsis,
                                       command=lambda bgclr=core.DEFAULT_SECOND_COLOR:
                                       [self.notebook.events.event_btnCreateOval(thickness=self.thickness,
                                                                                 bgcolor=bgclr,
                                                                                 outcolor=self.color_code[1]),
                                        self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_ellipsis, "Эллипсис")

        self.pic_line = image_resize((25, 20), f"images/{self.dir}/line.{self.format}")
        self.btn_line = ttk.Button(self.figure_labelframe,
                                   image=self.pic_line,
                                   command=lambda: [self.notebook.events.event_btnCreateLine(thickness=self.thickness,
                                                                                             color=self.color_code[1]),
                                                    self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_line, "Линия")

        self.pic_arrow = image_resize((25, 20), f"images/{self.dir}/arrow.{self.format}")
        self.btn_arrow = ttk.Button(self.figure_labelframe,
                                    image=self.pic_arrow,
                                    command=lambda:
                                    [self.notebook.events.event_btnCreateVector(thickness=self.thickness,
                                                                                color=self.color_code[1]),
                                     self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_arrow, "Вектор")

        self.pic_plot = image_resize((25, 20), f"images/{self.dir}/plot.{self.format}")
        self.btn_plot = ttk.Button(self.figure_labelframe,
                                   image=self.pic_plot,
                                   command=lambda: [self.notebook.events.event_btnCreateCoordinatePlane(),
                                                    self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_plot, "Координатная плоскость")

            # страница 2

        # self.filters_labelframe = ttk.Labelframe(self.toolbar_2, text="Фильтры")

            # filter1
        self.frame_filter1 = ttk.Labelframe(self.toolbar_2, text="Шумы")
        self.variable_filter_1 = StringVar(self.frame_filter1)
        self.variable_filter_1.set(core.DEFAULT_FILTERS_1[0])
        self.filters1 = ttk.OptionMenu(self.frame_filter1, self.variable_filter_1, *core.DEFAULT_FILTERS_1)
        self.btn_apply_filter1 = ttk.Button(self.frame_filter1,
                                            text="Применить",
                                            command=lambda
                                            x=self.variable_filter_1: [self.notebook.image_processing.apply_filter_1(x),
                                                                       self.notebook.set_save_label()])

            # filter3
        self.frame_filter3 = ttk.Labelframe(self.toolbar_2, text="Базовые фильтры")
        self.variable_filter_3 = StringVar(self.frame_filter3)
        self.variable_filter_3.set(core.DEFAULT_FILTERS_3[0])
        self.filters3 = ttk.OptionMenu(self.frame_filter3, self.variable_filter_3, *core.DEFAULT_FILTERS_3)
        self.btn_apply_filter3 = ttk.Button(self.frame_filter3,
                                            text="Применить",
                                            command=lambda
                                            x=self.variable_filter_3: [self.notebook.image_processing.apply_filter_3(x),
                                                                       self.notebook.set_save_label()])

            # filter2
        self.frame_filter2 = ttk.Labelframe(self.toolbar_2, text="Стандартные параметры")
        self.variable_filter_2 = StringVar(self.frame_filter2)
        self.variable_filter_2.set(core.DEFAULT_FILTERS_2[0])
        self.filters2 = ttk.OptionMenu(self.frame_filter2, self.variable_filter_2, *core.DEFAULT_FILTERS_2)
        self.filter_2_percent = ttk.Scale(self.frame_filter2, length=150, from_=0, to=500)
        self.filter_2_percent.set(100)
        self.filter_2_percent.bind("<Button-1>",
                                   lambda
                                   event,
                                   fl=self.variable_filter_2,
                                   scale=self.filter_2_percent:
                                   self.notebook.image_processing.apply_filter_2(f=fl, per=scale, event=event))
        self.btn_apply_filter2 = ttk.Button(self.frame_filter2,
                                            text="Применить",
                                            command=lambda: [self.notebook.image_processing.append_image(),
                                                             self.reset_scales(),
                                                             self.notebook.set_save_label()])
        self.value_label = ttk.Label(self.frame_filter2, text=100,  width=3)
        self.filter_2_percent.config(command=slider_filter2)
        self.ticks_label_filter2 = ttk.Label(self.frame_filter2, text='0     |    250    |    500',
                                             font=(self.font, 9))

            # filter4
        self.frame_filter4 = ttk.LabelFrame(self.toolbar_2, text='Работа с цветовыми слоями')
        self.r_scale_box = ttk.Scale(self.frame_filter4, length=130, from_=0, to=200, orient=HORIZONTAL)
        self.r_scale_box.set(100)
        self.g_scale_box = ttk.Scale(self.frame_filter4, length=130, from_=0, to=200, orient=HORIZONTAL)
        self.g_scale_box.set(100)
        self.b_scale_box = ttk.Scale(self.frame_filter4, length=130, from_=0, to=200, orient=HORIZONTAL)
        self.b_scale_box.set(100)

        self.label_r = ttk.Label(self.frame_filter4, text='R', width=2)
        self.label_g = ttk.Label(self.frame_filter4, text='G', width=2)
        self.label_b = ttk.Label(self.frame_filter4, text='B', width=2)
        self.r_scale_value = ttk.Label(self.frame_filter4, text='100 %', width=6)
        self.g_scale_value = ttk.Label(self.frame_filter4, text='100 %', width=6)
        self.b_scale_value = ttk.Label(self.frame_filter4, text='100 %', width=6)

        self.r_scale_box.config(command=slider_filter_r)
        self.g_scale_box.config(command=slider_filter_g)
        self.b_scale_box.config(command=slider_filter_b)

        self.ticks_label_filter4 = ttk.Label(self.frame_filter4,
                                             text='0   |  100  |  200',
                                             font=(self.font, 9))
        self.r_scale_box.bind("<Button-1>",
                              lambda
                              event,
                              r=self.r_scale_box,
                              g=self.g_scale_box,
                              b=self.b_scale_box: self.notebook.image_processing.change_layers(red=r,
                                                                                               green=g,
                                                                                               blue=b,
                                                                                               event=event))
        self.g_scale_box.bind("<Button-1>",
                              lambda
                              event,
                              r=self.r_scale_box,
                              g=self.g_scale_box,
                              b=self.b_scale_box: self.notebook.image_processing.change_layers(red=r,
                                                                                               green=g,
                                                                                               blue=b,
                                                                                               event=event))
        self.b_scale_box.bind("<Button-1>",
                              lambda
                              event,
                              r=self.r_scale_box,
                              g=self.g_scale_box,
                              b=self.b_scale_box: self.notebook.image_processing.change_layers(red=r,
                                                                                               green=g,
                                                                                               blue=b,
                                                                                               event=event))
        self.btn_apply_filter4 = ttk.Button(self.frame_filter4,
                                            text='Применить',
                                            command=lambda: [self.notebook.image_processing.append_image(),
                                                             self.reset_scales(),
                                                             self.notebook.set_save_label()])

            # filter5
        self.frame_filter5 = ttk.LabelFrame(self.toolbar_2, text='')
        self.btn_mix_layers = ttk.Button(self.frame_filter5,
                                         text="Перемешать слои",
                                         command=lambda: [self.notebook.image_processing.apply_filter_4(),
                                                          self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_mix_layers, "В случайном порядке перемешивает цветовые слои")
        self.btn_normalize = ttk.Button(self.frame_filter5,
                                        text="Нормализация",
                                        command=lambda: [self.notebook.image_processing.normalize_image(),
                                                         self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_normalize, "Нормализация изображения")

            # filter6
        self.frame_filter6 = ttk.LabelFrame(self.toolbar_2, text='Отразить')
        self.im_horizontal = image_resize((25, 20), f"images/{self.dir}/vertical.{self.format}")
        self.btn_apply_filter6_1 = ttk.Button(self.frame_filter6,
                                              image=self.im_horizontal,
                                              command=lambda:
                                              [self.notebook.image_processing.reflect_image('horizontal'),
                                               self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_apply_filter6_1, "Отразить по горизонтали")
        self.im_vertical = image_resize((25, 20), f"images/{self.dir}/horizontal.{self.format}")
        self.btn_apply_filter6_2 = ttk.Button(self.frame_filter6,
                                              image=self.im_vertical,
                                              command=lambda: [self.notebook.image_processing.reflect_image('vertical'),
                                                               self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_apply_filter6_2, "Отразить по вертикали")

            # filter7
        self.frame_filter7 = ttk.LabelFrame(self.toolbar_2, text='Повернуть')
        self.im_rotate_right = image_resize((25, 20), f"images/{self.dir}/rotate_right.{self.format}")
        self.btn_apply_filter7_1 = ttk.Button(self.frame_filter7,
                                              image=self.im_rotate_right,
                                              command=lambda: [self.notebook.image_processing.rotate_image('90'),
                                                               self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_apply_filter7_1, "Повернуть изображение на 90° вправо")
        self.im_rotate_left = image_resize((25, 20), f"images/{self.dir}/rotate_left.{self.format}")
        self.btn_apply_filter7_2 = ttk.Button(self.frame_filter7,
                                              image=self.im_rotate_left,
                                              command=lambda: [self.notebook.image_processing.rotate_image('-90'),
                                                               self.notebook.set_save_label()])
        _tool_tip.ToolTip(self.btn_apply_filter7_2, "Повернуть изображение на 90° влево")

        # упаковка виджетов

        self.btn_add_list.grid(row=0, column=0, sticky="WE")
        self.btn_back_list.grid(row=0, column=1, sticky="WE")
        self.btn_undo.grid(row=0, column=2, sticky="NSWE")
        self.btn_replace.grid(row=0, column=3, sticky="NSWE")
        self.btn_clear.grid(row=0, column=4, sticky="NSWE")

        self.btn_brush.grid(row=0, column=0, sticky="NSWE")
        self.btn_fill.grid(row=0, column=1, sticky="NSWE")
        self.btn_text.grid(row=1, column=0, sticky="NSWE")
        self.btn_eraser.grid(row=1, column=1, sticky="NSWE")

        ttk.Separator(self.toolbar_1, orient=VERTICAL).grid(row=0, column=2, rowspan=2, sticky="NSWE")

        self.btn_colorchoice.grid(row=0, column=4, rowspan=2, columnspan=2, sticky="NSWE")
        self.color_frame.grid(row=0, column=6, rowspan=2, sticky="NSWE")
        self.btn_color.pack(expand=1, fill=Y)

        self.thickness_labelframe.grid(row=0, column=8, rowspan=2, sticky="NSWE")
        self.btn_thickness_1.grid(row=0, column=0, sticky="NSWE")
        self.btn_thickness_2.grid(row=1, column=0, sticky="NSWE")
        self.btn_thickness_3.grid(row=2, column=0, sticky="NSWE")
        self.btn_thickness_4.grid(row=3, column=0, sticky="NSWE")
        self.thickness_scale.grid(row=0, column=1, rowspan=4, sticky="NSWE")
        self.thickness_value.grid(row=0, column=2, rowspan=4, sticky="WE")

        ttk.Separator(self.toolbar_1, orient=VERTICAL).grid(row=0, column=9, rowspan=2, sticky="NSWE")

        self.figure_labelframe.grid(row=0, column=10, rowspan=3, sticky="NS")
        self.btn_rectangle.grid(row=0, column=0)
        self.btn_polygon.grid(row=0, column=1)
        self.btn_ellipsis.grid(row=0, column=2)
        self.btn_line.grid(row=1, column=0)
        self.btn_arrow.grid(row=1, column=1)
        self.btn_plot.grid(row=1, column=2)

        self.frame_filter6.grid(row=0, column=0, sticky="NS")
        self.btn_apply_filter6_1.grid(row=0, column=0, sticky="WE")
        self.btn_apply_filter6_2.grid(row=0, column=1, sticky="WE")

        self.frame_filter7.grid(row=1, column=0, sticky="NS")
        self.btn_apply_filter7_1.grid(row=0, column=0, sticky="WE")
        self.btn_apply_filter7_2.grid(row=0, column=1, sticky="WE")

        ttk.Separator(self.toolbar_2, orient=VERTICAL).grid(row=0, column=2, rowspan=2, sticky="NSWE")

        # self.filters_labelframe.grid(row=0, column=3, rowspan=2, sticky="NS")
        self.frame_filter1.grid(row=0, column=3, rowspan=2, sticky="NSWE")
        self.filters1.grid(row=0, sticky="we")
        self.btn_apply_filter1.grid(row=1, sticky="e")

        self.frame_filter3.grid(row=0, column=4, rowspan=2, sticky="NSWE")
        self.filters3.grid(row=0, sticky="we")
        self.btn_apply_filter3.grid(row=1, sticky="e")

        ttk.Separator(self.toolbar_2, orient=VERTICAL).grid(row=0, column=5, rowspan=2, sticky="NSWE")

        self.frame_filter2.grid(row=0, column=6, rowspan=2, sticky="NSWE")
        self.filters2.grid(row=0, column=0, sticky="we")
        self.btn_apply_filter2.grid(row=0, column=1, sticky="e")

        self.filter_2_percent.grid(row=1, column=0, columnspan=2, sticky="NSWE")
        self.value_label.grid(row=1, column=2, sticky="NSWE")
        self.ticks_label_filter2.grid(row=2, column=0, columnspan=2, sticky="NSWE")

        ttk.Separator(self.toolbar_2, orient=VERTICAL).grid(row=0, column=7, rowspan=2, sticky="NSWE")

        self.frame_filter4.grid(row=0, column=8, rowspan=2, sticky="NSWE")
        self.label_r.grid(row=0, column=0)
        self.label_g.grid(row=1, column=0)
        self.label_b.grid(row=2, column=0)
        self.r_scale_box.grid(row=0, column=1)
        self.g_scale_box.grid(row=1, column=1)
        self.b_scale_box.grid(row=2, column=1)
        self.r_scale_value.grid(row=0, column=2)
        self.g_scale_value.grid(row=1, column=2)
        self.b_scale_value.grid(row=2, column=2)
        self.ticks_label_filter4.grid(column=1, row=3, columnspan=2, sticky="NSWE")
        self.btn_apply_filter4.grid(row=0, column=3, rowspan=3, sticky="WE")

        self.frame_filter5.grid(row=0, column=9, rowspan=2, sticky="NSWE")
        self.btn_mix_layers.grid(row=0, column=0, sticky="WE")
        self.btn_normalize.grid(row=1, column=0, sticky="WE")

        ttk.Separator(self.toolbar_2, orient=VERTICAL).grid(row=0, column=10, rowspan=2, sticky="NSWE")


if __name__ == "__main__":
    app = App()
    app.title('Visualist')
    app.state('zoomed')


    def change_theme_black():
        app.set_theme('black')
        btn_theme = ttk.Button(app.main_toolbar, image=app.moon, command=change_theme_white)
        _tool_tip.ToolTip(btn_theme, "Установить светлую тему")
        btn_theme.grid(row=0, column=5, sticky="NSWE")

    def change_theme_white():
        app.set_theme('arc')
        btn_theme = ttk.Button(app.main_toolbar, image=app.sun, command=change_theme_black)
        _tool_tip.ToolTip(btn_theme, "Установить тёмную тему")
        btn_theme.grid(row=0, column=5, sticky="NSWE")

    btn_theme = ttk.Button(app.main_toolbar, image=app.moon, command=change_theme_white)
    _tool_tip.ToolTip(btn_theme, "Установить светлую тему")
    btn_theme.grid(row=0, column=5, sticky="NSWE")

    def f(s):
        app.set_theme(str(s))

    options = StringVar(app.main_toolbar)
    menu = ttk.OptionMenu(app.main_toolbar, options,
                          "aquativo", "aquativo", "blue", "breeze", "clearlooks", "elegance", "equilux", "kroc",
                          "plastik", "radiance", "smog", "winxpblue", "yaru",
                          command=f)
    menu.grid(row=0, column=6, sticky="NSWE")

    app.mainloop()
