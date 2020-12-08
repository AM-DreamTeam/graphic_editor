from tkinter import *
from tkinter import Menu
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import tkinter.colorchooser
from random import choice

from core import core
from compressionRecognition import _core

class Settings(Toplevel):
    def __init__(self):
        super().__init__()
        self.init_child()

    def init_child(self):

        self.themes = {"Темная тема 1":("blacktheme1", "black"), "Темная тема 2":("blacktheme2", "black"),
                       "Светлая тема":("whitetheme", "arc")}

        ico = Image.open('images/visualist.png')
        ico.thumbnail((64, 64), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)

        self.sett_labelframe = ttk.LabelFrame(self, text="Персонализация")

        self.sett_1 = ttk.Label(self.sett_labelframe, text="Тема:")

        self.variable_theme = StringVar(self.sett_labelframe)
        self.variable_theme.set("Темная тема 1")
        self.sett_1_op = ttk.OptionMenu(self.sett_labelframe, StringVar(), self.variable_theme, *self.themes.keys())

        self.btn_apply_theme = ttk.Button(self.sett_labelframe, text="Применить",
                                          command=print(self.themes[self.variable_theme.get()][1]))





        self.sett_labelframe.grid(row=0, column=0, sticky="NSWE")

        self.sett_1.grid(row=0, column=0, sticky="NSWE")
        self.sett_1_op.grid(row=0, column=1, sticky="NSWE")
        self.btn_apply_theme.grid(row=0, column=2, sticky="NSWE")


        self.title('Настройки')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()


class App(Tk):
    def __init__(self, styler):
        super().__init__()
        self.init_main(styler)

        # лого
        ico = Image.open('images/visualist.png')
        ico.thumbnail((64, 64), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)

    def open_dialog(self):
        Settings()

    def init_main(self, styler):
        self.styler = styler

        # параметры стилизации
        self.dir = self.styler[0]
        self.stock_bg = self.styler[1]
        self.second_bg = self.styler[2]
        self.font = "courier"
        self.format = self.styler[3]

        # вспомогательные функции
        def image_resize(size: tuple, pic: str):
            return ImageTk.PhotoImage(Image.open(pic).resize(size))

        self.color_code = ((0.0, 0.0, 0.0), self.stock_bg)
        def choose_color():
            self.color_code = tkinter.colorchooser.askcolor(title="Цвета")
            self.btn_color.config(bg=self.color_code[1])

        def slider_filter2(value):
            self.value_label.config(text=round(float(value)))
        def slider_filter_r(value):
            self.r_scale_value.config(text=f'R {round(float(value))}')
        def slider_filter_g(value):
            self.g_scale_value.config(text=f'G {round(float(value))}')
        def slider_filter_b(value):
            self.b_scale_value.config(text=f'B {round(float(value))}')


        self.thickness = 5
        def slider_thickness(value):
            self.thickness_value.config(text=round(float(value)))
            self.thickness = round(float(value))

        self.mdeb = 100
        def slider_compression(value):
            self.compression_value.config(text=f'{round(float(value))} %')
            self.mdeb = str(round(float(value)))

        # стили
        self.styler = ttk.Style()
        self.styler.configure("TButton", foreground=None, background=None, relief="flat")
        self.styler.configure("TSeparator", foreground=None, background=None)
        self.styler.configure('Red.TLabelframe.Label', font=(self.font, 12), foreground=self.stock_bg, background=self.second_bg)
        self.styler.configure("Red.TLabelframe", foreground="red", background=self.stock_bg)

        # создание холста
        self.notebook = core.CustomNotebook(self)
        self.notebook.grid(row=2, column=0, rowspan=2, sticky="nsew")

        # меню
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=-2)
        self.filemenu.add_command(label="Открыть...", command=lambda: self.notebook.image_processing.set_image())
        self.filemenu.add_command(label="Сохранить...", command=lambda: self.notebook.image_processing.save_image())
        self.filemenu.add_command(label="Настройки", command=self.open_dialog)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Выход", command=self.quit)
        self.menubar.add_cascade(label="Файл", menu=self.filemenu)

        self.menubar.add_command(label='Новый холст', command=self.notebook.create_new_canvas)
        self.menubar.add_command(label='Вернуть хост', command=lambda:self.notebook.reestablish_tab())
        self.menubar.add_command(label='Инфо', command=lambda:self.notebook.image_processing.get_info())

        self.config(menu=self.menubar)

        self.notebook.bind("<<NotebookTabChanged>>", self.notebook.select_curr_tab)
        self.bind('<Control-z>', lambda e: self.notebook.undo(e))
        self.bind('<Control-x>', quit)

        # изменине окна
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

        # GUI виджеты
        self.nb = ttk.Notebook(self, width=900, height=110)
        self.toolbar_1 = ttk.Frame(self.nb)
        self.toolbar_2 = ttk.Frame(self.nb)
        self.toolbar_3 = ttk.Frame(self.nb)
        self.nb.add(self.toolbar_1, text='graphic_lib')
        self.nb.add(self.toolbar_2, text='image_lib')
        self.nb.add(self.toolbar_3, text='text_recognition')

        self.main_toolbar = ttk.Frame(self)

        self.main_toolbar.grid(row=1, column=0, sticky="WE")
        self.nb.grid(row=0, column=0, sticky="WE")

            # панель

        self.im_undo = image_resize((20, 20), f"images/{self.dir}/undo.{self.format}")
        self.btn_undo = ttk.Button(self.main_toolbar, style="TButton", image=self.im_undo)

        self.im_redo = image_resize((20, 20), f"images/{self.dir}/redo.{self.format}")
        self.btn_redo = ttk.Button(self.main_toolbar, style="TButton", image=self.im_redo)

        self.im_replace = image_resize((20, 20), f"images/{self.dir}/replace.{self.format}")
        self.btn_replace = ttk.Button(self.main_toolbar, style="TButton", image=self.im_replace,
                                      command=lambda: self.notebook.events.event_move())

        self.im_clear = image_resize((20, 20), f"images/{self.dir}/delete.{self.format}")
        self.btn_clear = ttk.Button(self.main_toolbar, style="TButton", image=self.im_clear,
                                    command=lambda: self.notebook.events.event_btnClear())


            # страница 1

        self.im_brush = image_resize((30, 30), f"images/{self.dir}/brush.{self.format}")
        self.btn_brush = ttk.Button(self.toolbar_1, style="TButton", image=self.im_brush,
                                    command=lambda:
                                    self.notebook.events.event_btnBrush(size=self.thickness, color=self.color_code[1], debug_mode=False)
                                    )

        self.im_fill = image_resize((30, 30), f"images/{self.dir}/fill.{self.format}")
        self.btn_fill = ttk.Button(self.toolbar_1, style="TButton", image=self.im_fill,
                                   command=lambda:
                                   self.notebook.events.event_btnFill(color=self.color_code[1])
                                   )

        self.im_text = image_resize((30, 30), f"images/{self.dir}/text.{self.format}")
        self.btn_text = ttk.Button(self.toolbar_1, style="TButton", image=self.im_text,
                                   command=lambda:self.notebook.events.event_btnCreateText())

        self.im_eraser = image_resize((30, 30), f"images/{self.dir}/eraser.{self.format}")
        self.btn_eraser = ttk.Button(self.toolbar_1, style="TButton", image=self.im_eraser,
                                     command=lambda:self.notebook.events.event_btnQuickEraser())


        self.sep_1 = ttk.Separator(self.toolbar_1, style="TSeparator", orient=VERTICAL)


        self.im_color = image_resize((70, 70), f"images/{self.dir}/color.{self.format}")
        self.btn_colorchoice = ttk.Button(self.toolbar_1, style="TButton", image=self.im_color, command=choose_color)

        self.color_frame = ttk.Frame(self.toolbar_1)
        self.btn_color = Button(self.color_frame, bg=self.color_code[1])



        self.sep_2 = ttk.Separator(self.toolbar_1, style="TSeparator", orient=VERTICAL)


        self.thickness_labelframe = ttk.Labelframe(self.toolbar_1, text="Толщина", style="Red.TLabelframe")

        self.pic_thickness_1 = image_resize((100, 8), f"images/{self.dir}/lineth1.jpg")
        self.btn_thickness_1 = ttk.Button(self.thickness_labelframe, image=self.pic_thickness_1, style="TButton",
                                          command=lambda: [self.notebook.events.event_btnThickness(thickness=5),
                                                           self.thickness_value.config(text=5),
                                                           self.thickness_scale.set(5)])

        self.pic_thickness_2 = image_resize((100, 8), f"images/{self.dir}/lineth2.jpg")
        self.btn_thickness_2 = ttk.Button(self.thickness_labelframe, image=self.pic_thickness_2, style="TButton",
                                          command=lambda: [self.notebook.events.event_btnThickness(thickness=10),
                                                           self.thickness_value.config(text=10),
                                                           self.thickness_scale.set(10)])

        self.pic_thickness_3 = image_resize((100, 8), f"images/{self.dir}/lineth3.jpg")
        self.btn_thickness_3 = ttk.Button(self.thickness_labelframe, image=self.pic_thickness_3, style="TButton",
                                          command=lambda: [self.notebook.events.event_btnThickness(thickness=15),
                                                           self.thickness_value.config(text=15),
                                                           self.thickness_scale.set(15)])

        self.pic_thickness_4 = image_resize((100, 8), f"images/{self.dir}/lineth4.jpg")
        self.btn_thickness_4 = ttk.Button(self.thickness_labelframe, image=self.pic_thickness_4, style="TButton",
                                          command=lambda: [self.notebook.events.event_btnThickness(thickness=20),
                                                           self.thickness_value.config(text=20),
                                                           self.thickness_scale.set(20)])

        self.thickness_value = Label(self.thickness_labelframe, text=self.thickness, anchor=N, bg=self.stock_bg,
                                     foreground=self.second_bg,
                                     font=("Comic Sans MS", 15, "bold"))
        self.thickness_scale = ttk.Scale(self.thickness_labelframe, orient=VERTICAL, length=50, from_=1, to=20,
                                         command=slider_thickness)
        self.thickness_label = ttk.Label(self.thickness_labelframe, text='0     100     200     300     400     500')
        self.btn_apply_thickness = ttk.Button(self.thickness_labelframe, text="Применить",
                                             command=lambda:
                                             self.notebook.events.event_btnThickness(thickness=self.thickness))


        self.sep_3 = ttk.Separator(self.toolbar_1, style="TSeparator", orient=VERTICAL)


        self.figure_labelframe = ttk.Labelframe(self.toolbar_1, text="Фигуры", style="Red.TLabelframe")

        self.pic_rectangle = image_resize((25, 20), f"images/{self.dir}/rectangle.{self.format}")
        self.btn_rectangle = ttk.Button(self.figure_labelframe, image=self.pic_rectangle, style="TButton",
                                        command=lambda bgclr=core.DEFAULT_SECOND_COLOR:
                                        self.notebook.events.event_btnCreateRectangle(thickness=self.thickness, bgcolor=bgclr,
                                                                                 outcolor=self.color_code[1]))

        self.pic_polygon = image_resize((25, 20), f"images/{self.dir}/polygon.{self.format}")
        self.btn_polygon = ttk.Button(self.figure_labelframe, image=self.pic_polygon, style="TButton",
                                      command=lambda bgclr=core.DEFAULT_SECOND_COLOR:
                                      self.notebook.events.event_btnCreatePolygon(thickness=self.thickness, bgcolor=bgclr,
                                                                             outcolor=self.color_code[1]))

        self.pic_ellipsis = image_resize((25, 20), f"images/{self.dir}/ellipsis.{self.format}")
        self.btn_ellipsis = ttk.Button(self.figure_labelframe, image=self.pic_ellipsis, style="TButton",
                                       command=lambda bgclr=core.DEFAULT_SECOND_COLOR:
                                       self.notebook.events.event_btnCreateOval(thickness=self.thickness, bgcolor=bgclr,
                                                                                outcolor=self.color_code[1]))

        self.pic_line = image_resize((25, 20), f"images/{self.dir}/line.{self.format}")
        self.btn_line = ttk.Button(self.figure_labelframe, image=self.pic_line, style="TButton",
                                   command=lambda:self.notebook.events.event_btnCreateLine(thickness=self.thickness,
                                                                            color=self.color_code[1]))

        self.pic_arrow = image_resize((25, 20), f"images/{self.dir}/arrow.{self.format}")
        self.btn_arrow = ttk.Button(self.figure_labelframe, image=self.pic_arrow, style="TButton",
                                    command=lambda:self.notebook.events.event_btnCreateVector(thickness=self.thickness,
                                                                                              color=self.color_code[1]))

        self.pic_plot = image_resize((25, 20), f"images/{self.dir}/plot.{self.format}")
        self.btn_plot = ttk.Button(self.figure_labelframe, image=self.pic_plot, style="TButton",
                                    command=lambda:self.notebook.events.event_btnCreateCoordinatePlane())
            # страница 2

        self.im_return = image_resize((30, 30), f"images/{self.dir}/return.{self.format}")
        self.btn_return = ttk.Button(self.toolbar_2, image=self.im_return, style="TButton",
                                    )

        self.im_add_list = image_resize((30, 30), f"images/{self.dir}/add_list.{self.format}")
        self.btn_add_list = ttk.Button(self.toolbar_2, text="Добавить холст", image=self.im_add_list, compound=LEFT,
                                       style="TButton",
                                       )

        self.filters_labelframe = ttk.Labelframe(self.toolbar_2, text="Фильтры", style="Red.TLabelframe")

            # filter1
        self.frame_filter1 = ttk.Labelframe(self.filters_labelframe, text="Шумы")
        self.variable_filter_1 = StringVar(self.frame_filter1)
        self.variable_filter_1.set(core.DEFAULT_FILTERS_1[0])
        self.filters1 = ttk.OptionMenu(self.frame_filter1, self.variable_filter_1, *core.DEFAULT_FILTERS_1)
        self.btn_apply_filter1 = ttk.Button(self.frame_filter1, text="Применить",
                                            command=lambda x=self.variable_filter_1:
                                            self.notebook.image_processing.apply_filter_1(x))

            # filter3
        self.frame_filter3 = ttk.Labelframe(self.filters_labelframe, text="Базовые фильтры")
        self.variable_filter_3 = StringVar(self.frame_filter3)
        self.variable_filter_3.set(core.DEFAULT_FILTERS_3[0])
        self.filters3 = ttk.OptionMenu(self.frame_filter3, self.variable_filter_3, *core.DEFAULT_FILTERS_3)
        self.btn_apply_filter3 = ttk.Button(self.frame_filter3, text="Применить",
                                            command=lambda x=self.variable_filter_3:
                                            self.notebook.image_processing.apply_filter_3(x))

            # filter2
        self.frame_filter2 = ttk.Labelframe(self.filters_labelframe, text="Стандартные параметры")
        self.variable_filter_2 = StringVar(self.frame_filter2)
        self.variable_filter_2.set(core.DEFAULT_FILTERS_2[0])
        self.filters2 = ttk.OptionMenu(self.frame_filter2, self.variable_filter_2, *core.DEFAULT_FILTERS_2)
        self.filter_2_percent = ttk.Scale(self.frame_filter2, length=150, from_=0, to=500)
        self.filter_2_percent.set(100)
        self.filter_2_percent.bind("<B1-Motion>", lambda
            event,
            f=self.variable_filter_2,
            scale=self.filter_2_percent:
        self.notebook.image_processing.apply_filter_2(f=f, per=scale, event=event))
        self.btn_apply_filter2 = ttk.Button(self.frame_filter2, text="Применить",
                                            command=lambda: [self.notebook.image_processing.append_image(),
                                                             self.reset_scales()])
        self.value_label = ttk.Label(self.frame_filter2, text=100)
        self.filter_2_percent.config(command = slider_filter2)

        self.kastyl = ttk.Label(self.frame_filter2, text="      ")
        self.ticks_label_filter2 = ttk.Label(self.frame_filter2, text='0     |    250    |    500',
                                             font=(self.font, 9))

            # filter4
        self.frame_filter4 = ttk.LabelFrame(self.filters_labelframe, text='Работа с цветовыми слоями')
        self.r_scale_box = ttk.Scale(self.frame_filter4, length=130, from_=0, to=200, orient=HORIZONTAL)
        self.r_scale_box.set(100)
        self.g_scale_box = ttk.Scale(self.frame_filter4, length=130, from_=0, to=200, orient=HORIZONTAL)
        self.g_scale_box.set(100)
        self.b_scale_box = ttk.Scale(self.frame_filter4, length=130, from_=0, to=200, orient=HORIZONTAL)
        self.b_scale_box.set(100)

        self.r_scale_value = ttk.Label(self.frame_filter4, text='R 100')
        self.g_scale_value = ttk.Label(self.frame_filter4, text='G 100')
        self.b_scale_value = ttk.Label(self.frame_filter4, text='B 100')

        self.r_scale_box.config(command=slider_filter_r)
        self.g_scale_box.config(command=slider_filter_g)
        self.b_scale_box.config(command=slider_filter_b)

        self.ticks_label_filter4 = ttk.Label(self.frame_filter4, text='0   |  100  |  200     ',
                                     font=(self.font, 9))
        self.r_scale_box.bind("<B1-Motion>",
                              lambda
                                  event,
                                  r=self.r_scale_box,
                                  g=self.g_scale_box,
                                  b=self.b_scale_box:
                              self.notebook.image_processing.change_layers(red=r, green=g, blue=b, event=event))
        self.g_scale_box.bind("<B1-Motion>", lambda
            event,
            r=self.r_scale_box,
            g=self.g_scale_box,
            b=self.b_scale_box:
        self.notebook.image_processing.change_layers(red=r, green=g, blue=b, event=event))
        self.b_scale_box.bind("<B1-Motion>", lambda
            event,
            r=self.r_scale_box,
            g=self.g_scale_box,
            b=self.b_scale_box:
        self.notebook.image_processing.change_layers(red=r, green=g, blue=b, event=event))
        self.btn_apply_filter4 = ttk.Button(self.frame_filter4,
               text='Применить',
               command=lambda: [self.notebook.image_processing.append_image(), self.reset_scales()]
               )

            # filter5
        self.frame_filter5 = ttk.LabelFrame(self.filters_labelframe, text='')
        self.btn_mix_layers = ttk.Button(self.frame_filter5,text="mix layers",
                                         command=lambda: self.notebook.image_processing.apply_filter_4())
        self.btn_normalize = ttk.Button(self.frame_filter5, text="normalize",
                                        command=lambda: self.notebook.image_processing.normalize_image())

            # filter6
        self.frame_filter6 = ttk.LabelFrame(self.filters_labelframe, text='Отразить')
        self.btn_apply_filter6_1 = ttk.Button(self.frame_filter6,text="horizontal",
                                     command=lambda:self.notebook.image_processing.reflect_image('horizontal'))
        self.btn_apply_filter6_2 = ttk.Button(self.frame_filter6,text="vertical",
                                     command=lambda:self.notebook.image_processing.reflect_image('vertical'))

            # filter7
        self.frame_filter7 = ttk.LabelFrame(self.filters_labelframe, text='Повернуть')
        self.btn_apply_filter7_1 = ttk.Button(self.frame_filter7,text="90",
                                     command=lambda:self.notebook.image_processing.rotate_image('90'))
        self.btn_apply_filter7_2 = ttk.Button(self.frame_filter7,text="-90",
                                     command=lambda:self.notebook.image_processing.rotate_image('-90'))






            # страница 3

        self.textRecognition = ttk.Label(self.toolbar_3)

        tr = _core.Features(self.textRecognition, self.mdeb)

        self.btn_recognition = ttk.Button(self.toolbar_3, text="распознание текста", command=tr.recognitionText)
        self.btn_compression = ttk.Button(self.toolbar_3, text="сжатие изображения", command=tr.imageСompression)

        self.compression_value = ttk.Label(self.toolbar_3, text="100 %")
        self.compression_scale = ttk.Scale(self.toolbar_3, length=200, from_=100, to=1000, command=slider_compression)
        self.compression_label = ttk.Label(self.toolbar_3, text='100         |            500            |             1000')

        self.btn_recognition.grid(row=0, column=1, sticky="NSWE")
        self.btn_compression.grid(row=0, column=0, sticky="NSWE")

        self.compression_scale.grid(row=1, column=0, sticky="NSWE")
        self.compression_value.grid(row=1, column=1, sticky="NSWE")
        self.compression_label.grid(row=2, column=0, sticky="NSWE")

        # упаковка виджетов

        self.btn_undo.grid(row=0, column=0, sticky="NSWE")
        self.btn_redo.grid(row=0, column=1, sticky="NSWE")
        self.btn_replace.grid(row=0, column=2, sticky="NSWE")
        self.btn_clear.grid(row=0, column=3, sticky="NSWE")

        self.btn_brush.grid(column=0, row=0, sticky="NSWE")
        self.btn_fill.grid(column=1, row=0, sticky="NSWE")
        self.btn_text.grid(column=0, row=1, sticky="NSWE")
        self.btn_eraser.grid(column=1, row=1, sticky="NSWE")

        # self.sep_1.grid(row=0, column=2, rowspan=2, sticky="NSWE")

        self.btn_colorchoice.grid(row=0, column=4, rowspan=2, columnspan=2, sticky="NSWE")
        self.color_frame.grid(row=0, column=6, rowspan=2, sticky="NSWE")
        self.btn_color.pack(expand=1, fill=Y)

        self.sep_2.grid(row=0, column=7, rowspan=2, sticky="NSWE")

        self.thickness_labelframe.grid(row=0, column=8, rowspan=2, sticky="NSWE")
        self.btn_thickness_1.grid(row=0, column=0, sticky="NSWE")
        self.btn_thickness_2.grid(row=1, column=0, sticky="NSWE")
        self.btn_thickness_3.grid(row=2, column=0, sticky="NSWE")
        self.btn_thickness_4.grid(row=3, column=0, sticky="NSWE")
        self.thickness_scale.grid(row=0, column=1, rowspan=4, sticky="NSWE")
        self.thickness_value.grid(row=0, column=2, rowspan=4, sticky="WE")
        self.btn_apply_thickness.grid(row=2, column=2, rowspan=2, sticky="WE")

        self.sep_3.grid(row=0, column=9, rowspan=2, sticky="NSWE")

        self.figure_labelframe.grid(row=0, column=10, rowspan=3, sticky="NS")
        self.btn_rectangle.grid(row=0, column=0)
        self.btn_polygon.grid(row=0, column=1)
        self.btn_ellipsis.grid(row=0, column=2)
        self.btn_line.grid(row=1, column=0)
        self.btn_arrow.grid(row=1, column=1)
        self.btn_plot.grid(row=1, column=2)

        self.btn_return.grid(column=0, row=0, rowspan=2, sticky="NS")
        self.btn_add_list.grid(column=1, row=0, rowspan=2, sticky="NS")

        self.filters_labelframe.grid(column=2, row=0, rowspan=2, sticky="NS")

        self.frame_filter1.grid(column=0, row=0, sticky="NSWE")
        self.filters1.grid(row=0, sticky="we")
        self.btn_apply_filter1.grid(row=1, sticky="e")

        self.frame_filter3.grid(column=1, row=0, sticky="NSWE")
        self.filters3.grid(row=0, sticky="we")
        self.btn_apply_filter3.grid(row=1, sticky="e")

        self.frame_filter2.grid(column=2, row=0, sticky="NSWE")
        self.filters2.grid(row=0, column=0, sticky="we")
        self.btn_apply_filter2.grid(row=0, column=1, sticky="e")
        self.kastyl.grid(row=0, column=2, sticky="e")

        self.filter_2_percent.grid(column=0, row=1, columnspan=2, sticky="NSWE")
        self.value_label.grid(column=2, row=1, sticky="NSWE")
        self.ticks_label_filter2.grid(column=0, row=2, columnspan=2, sticky="NSWE")


        self.frame_filter4.grid(row=0, column=3, sticky="NSWE")
        self.r_scale_box.grid(row=0, column=0, sticky="e")
        self.g_scale_box.grid(row=1, column=0, sticky="e")
        self.b_scale_box.grid(row=2, column=0, sticky="e")
        self.r_scale_value.grid(row=0, column=1, sticky="e")
        self.g_scale_value.grid(row=1, column=1, sticky="e")
        self.b_scale_value.grid(row=2, column=1, sticky="e")
        self.ticks_label_filter4.grid(column=0, row=3, columnspan=2, sticky="NSWE")
        self.btn_apply_filter4.grid(row=0, column=2, rowspan=3, sticky="WE")

        self.frame_filter5.grid(row=0, column=4, sticky="NSWE")
        self.btn_mix_layers.grid(row=0, column=0, sticky="WE")
        self.btn_normalize.grid(row=1, column=0, sticky="WE")

        self.frame_filter6.grid(row=0, column=5, sticky="NSWE")
        self.btn_apply_filter6_1.grid(row=0, column=0, sticky="WE")
        self.btn_apply_filter6_2.grid(row=1, column=0, sticky="WE")

        self.frame_filter7.grid(row=0, column=6, sticky="NSWE")
        self.btn_apply_filter7_1.grid(row=0, column=0, sticky="WE")
        self.btn_apply_filter7_2.grid(row=0, column=1, sticky="WE")

    def reset_scales(self, _=None):
        """
            Сбрасывает значения Scale до 100 при смене вкладки
        """
        self.filter_2_percent.set(100)
        self.r_scale_box.set(100)
        self.g_scale_box.set(100)
        self.b_scale_box.set(100)










if __name__ == "__main__":
    app = App(("blacktheme1", '#424242', 'black', 'jpg'))
    app.title('Visualist')
    app.state('zoomed')

    ThemedStyle(app, theme='black')


    def change_theme():
        app.init_main(("whitetheme", '#f5f6f7', 'black', 'jpg'))
        ThemedStyle(app, theme='arc')

    btn_theme = ttk.Button(app.main_toolbar, text='CT', command=change_theme)
    btn_theme.grid(row=0, column=4, sticky="NSWE")

    app.mainloop()
    #breeze, black, arc, aquativo
