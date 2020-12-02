from tkinter import *
from tkinter import Menu
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import tkinter.colorchooser
from random import choice, sample

from core import core




class App(Tk):
    def __init__(self):
        super().__init__()

        # лого
        ico = Image.open('images/visualist.png')
        ico.thumbnail((64, 64), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)

        # вспомогательные функции
        def image_resize(size: tuple, pic: str):
            return ImageTk.PhotoImage(Image.open(pic).resize(size))

        self.color_code = ((0.0, 0.0, 0.0), '#424242')
        def choose_color():
            self.color_code = tkinter.colorchooser.askcolor(title="Цвета")
            print(self.color_code[1])

        def ttk_slider_callback(value):
            self.value_label.config(text=round(float(value)))
            self.variable_filter_2_percent.set(round(float(value)))


        # параметры стилизации
        self.dir = "blacktheme2"
        self.stock_bg = self.color_code[1]
        self.second_bg = "red"
        self.font = "courier"

        # стили
        self.styler = ttk.Style()
        self.styler.configure("TButton", foreground="black", background=self.stock_bg, relief="flat")
        self.styler.configure("TSeparator", foreground="red", background="red")
        self.styler.configure('Red.TLabelframe.Label', font=(self.font, 12), foreground="black", background=self.stock_bg)
        self.styler.configure("Red.TLabelframe", foreground="red", background=self.stock_bg)

        # создание холста

        self.notebook = core.CustomNotebook(self)
        self.notebook.grid(row=2, column=0, rowspan=2, sticky="nsew")

        events = core.Events(self, core.DEFAULT_USED_EVENTS, self.notebook)
        thickness_list = sample(range(5, 20), 6)
        events.event_onCanvas()
        events.event_undo()

        # меню
        menubar = Menu(self)
        self.filemenu = Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Открыть...", command=lambda: self.notebook.image_processing.set_image())
        self.filemenu.add_command(label="Сохранить...", command=lambda: self.notebook.image_processing.save_image())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Выход", command=self.quit)
        menubar.add_cascade(label="Файл", menu=self.filemenu)
        self.config(menu=menubar)

        self.notebook.bind("<<NotebookTabChanged>>", self.notebook.select_curr_tab)

        # изменине окна
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

        # GUI виджеты
        self.nb = ttk.Notebook(self, width=900, height=90)
        self.toolbar_1 = ttk.Frame(self.nb)
        self.toolbar_2 = ttk.Frame(self.nb)
        self.nb.add(self.toolbar_1, text='graphic_lib')
        self.nb.add(self.toolbar_2, text='image_lib')

        self.main_toolbar = ttk.Frame(self)

        self.main_toolbar.grid(row=1, column=0, sticky="WE")
        self.nb.grid(row=0, column=0, sticky="WE")

            # страница 1

        self.im_brush = image_resize((30, 30), f"images/{self.dir}/brush.jpg")
        self.btn_brush = ttk.Button(self.toolbar_1, style="TButton", image=self.im_brush,
                                    command=lambda s=core.DEFAULT_BRUSH_SIZE, clr=core.DEFAULT_FIRST_COLOR:
                                    self.notebook.events.event_btnBrush(size=s, color=clr, debug_mode=False))

        self.im_fill = image_resize((30, 30), f"images/{self.dir}/fill.jpg")
        self.btn_fill = ttk.Button(self.toolbar_1, style="TButton", image=self.im_fill,
                                   command=lambda:self.notebook.events.event_btnFill(color=self.color_code[1]))

        self.im_text = image_resize((30, 30), f"images/{self.dir}/text.jpg")
        self.btn_text = ttk.Button(self.toolbar_1, style="TButton", image=self.im_text)

        self.im_eraser = image_resize((30, 30), f"images/{self.dir}/eraser.jpg")
        self.btn_eraser = ttk.Button(self.toolbar_1, style="TButton", image=self.im_eraser,
                                     command=self.notebook.events.event_btnQuickEraser)

        self.sep_1 = ttk.Separator(self.toolbar_1, style="TSeparator", orient=VERTICAL)

        self.im_color = image_resize((70, 70), f"images/{self.dir}/color.jpg")
        self.btn_colorchoice = ttk.Button(self.toolbar_1, style="TButton", image=self.im_color, command=choose_color)

        self.sep_2 = ttk.Separator(self.toolbar_1, style="TSeparator", orient=VERTICAL)

        self.im_replace = image_resize((20, 20), f"images/{self.dir}/replace.jpg")
        self.btn_replace = ttk.Button(self.main_toolbar, style="TButton", image=self.im_replace,
                                      command=lambda ms=core.DEFAULT_MOUSE_SPEED:
                                      self.notebook.events.event_move(mouse_speed=ms))

        self.im_clear = image_resize((20, 20), f"images/{self.dir}/delete.jpg")
        self.btn_clear = ttk.Button(self.main_toolbar, style="TButton", image=self.im_clear,
                                    command=lambda: self.notebook.events.event_btnClear())

        self.im_undo = image_resize((20, 20), f"images/{self.dir}/undo.jpg")
        self.btn_undo = ttk.Button(self.main_toolbar, style="TButton", image=self.im_undo)

        self.im_redo = image_resize((20, 20), f"images/{self.dir}/redo.jpg")
        self.btn_redo = ttk.Button(self.main_toolbar, style="TButton", image=self.im_redo)

        self.sep_3 = ttk.Separator(self.toolbar_1, style="TSeparator", orient=VERTICAL)

        self.figure_labelframe = ttk.Labelframe(self.toolbar_1, text="Фигуры", style="Red.TLabelframe")

        self.pic_rectangle = image_resize((25, 20), f"images/{self.dir}/rectangle.jpg")
        self.btn_rectangle = ttk.Button(self.figure_labelframe, image=self.pic_rectangle, style="TButton",
                                        command=lambda t=core.DEFAULT_THICKNESS, outclr=core.DEFAULT_FIRST_COLOR,
                                                       bgclr=core.DEFAULT_SECOND_COLOR:
                                        self.notebook.events.event_btnCreateRectangle(thickness=t, bgcolor=bgclr,
                                                                                 outcolor=outclr)
                                        )

        self.pic_line = image_resize((25, 20), f"images/{self.dir}/line.jpg")
        self.btn_line = ttk.Button(self.figure_labelframe, image=self.pic_line, style="TButton",
                                   command=lambda t=core.DEFAULT_THICKNESS, clr=core.DEFAULT_FIRST_COLOR:
                                   self.notebook.events.event_btnCreateLine(thickness=t, color=clr)
                                   )

        self.pic_ellipsis = image_resize((25, 20), f"images/{self.dir}/ellipsis.jpg")
        self.btn_ellipsis = ttk.Button(self.figure_labelframe, image=self.pic_ellipsis, style="TButton",
                                       command=lambda t=core.DEFAULT_THICKNESS, outclr=core.DEFAULT_FIRST_COLOR,
                                              bgclr=core.DEFAULT_SECOND_COLOR:
                                       self.notebook.events.event_btnCreateOval(thickness=t, bgcolor=bgclr, outcolor=outclr))

        self.pic_polygon = image_resize((25, 20), f"images/{self.dir}/polygon.jpg")
        self.btn_polygon = ttk.Button(self.figure_labelframe, image=self.pic_polygon, style="TButton",
                                      command=lambda t=core.DEFAULT_THICKNESS, outclr=core.DEFAULT_FIRST_COLOR,
                                                     bgclr=core.DEFAULT_SECOND_COLOR:
                                      self.notebook.events.event_btnCreatePolygon(thickness=t, bgcolor=bgclr,
                                                                                  outcolor=outclr))

            # страница 2

        self.im_return = image_resize((30, 30), f"images/{self.dir}/return.jpg")
        self.btn_return = ttk.Button(self.toolbar_2, image=self.im_return, style="TButton",
                                    command=lambda: self.notebook.image_processing.return_image())

        self.im_add_list = image_resize((30, 30), f"images/{self.dir}/add_list.jpg")
        self.btn_add_list = ttk.Button(self.toolbar_2, text="Добавить холст", image=self.im_add_list, compound=LEFT,
                                       style="TButton",
                                       command=self.notebook.create_new_canvas)

        self.filters_labelframe = ttk.Labelframe(self.toolbar_2, text="Фильтры", style="Red.TLabelframe")

        self.frame_filter1 = ttk.Frame(self.filters_labelframe)
        self.variable_filter_1 = StringVar(self.frame_filter1)
        self.variable_filter_1.set(core.DEFAULT_FILTERS_1[0])
        self.filters1 = ttk.OptionMenu(self.frame_filter1, self.variable_filter_1, *core.DEFAULT_FILTERS_1)
        self.btn_apply_filter1 = ttk.Button(self.frame_filter1, text="Применить",
                                            command=lambda x=self.variable_filter_1:
                                            self.notebook.image_processing.apply_filter_1(x))

        self.frame_filter3 = ttk.Frame(self.filters_labelframe)
        self.variable_filter_3 = StringVar(self.frame_filter3)
        self.variable_filter_3.set(core.DEFAULT_FILTERS_3[0])
        self.filters3 = ttk.OptionMenu(self.frame_filter3, self.variable_filter_3, *core.DEFAULT_FILTERS_3)
        self.btn_apply_filter3 = ttk.Button(self.frame_filter3, text="Применить",
                                            command=lambda x=self.variable_filter_3:
                                            self.notebook.image_processing.apply_filter_3(x))

        self.frame_filter2 = ttk.Frame(self.filters_labelframe)
        self.variable_filter_2 = StringVar(self.frame_filter2)
        self.variable_filter_2.set(core.DEFAULT_FILTERS_2[0])
        self.filters2 = ttk.OptionMenu(self.frame_filter2, self.variable_filter_2, *core.DEFAULT_FILTERS_2)
        self.variable_filter_2_percent = StringVar(self.frame_filter2)
        self.variable_filter_2_percent.set(100)
        self.btn_apply_filter2 = ttk.Button(self.frame_filter2, text="Применить",
                                            command=lambda
                                                x=self.variable_filter_2,
                                                y=self.variable_filter_2_percent:
                                            self.notebook.image_processing.apply_filter_2(x, y))


        self.value_label = ttk.Label(self.frame_filter2, text=0)
        self.scale = ttk.Scale(self.frame_filter2, length=150, from_=0, to=500, command=ttk_slider_callback)
        self.ticks_label = ttk.Label(self.frame_filter2, text='0     100     200     300     400     500')


        # упаковка виджетов


        self.btn_brush.grid(column=0, row=0, sticky="NSWE")
        self.btn_fill.grid(column=1, row=0, sticky="NSWE")
        self.btn_text.grid(column=0, row=1, sticky="NSWE")
        self.btn_eraser.grid(column=1, row=1, sticky="NSWE")

        self.sep_1.grid(row=0, column=2, rowspan=2, sticky="NSWE")

        self.btn_colorchoice.grid(row=0, column=4, rowspan=2, columnspan=2, sticky="NSWE")

        self.sep_2.grid(row=0, column=6, rowspan=2, sticky="NSWE")

        self.btn_replace.grid(row=0, column=2, sticky="NSWE")
        self.btn_clear.grid(row=0, column=3, sticky="NSWE")
        self.btn_undo.grid(row=0, column=0, sticky="NSWE")
        self.btn_redo.grid(row=0, column=1, sticky="NSWE")

        self.sep_3.grid(row=0, column=9, rowspan=2, sticky="NSWE")

        self.figure_labelframe.grid(row=0, column=10, rowspan=3, sticky="NS")
        self.btn_rectangle.grid(row=0, column=0)
        self.btn_line.grid(row=0, column=1)
        self.btn_ellipsis.grid(row=0, column=2)
        self.btn_polygon.grid(row=1, column=1)

        self.btn_return.grid(column=0, row=0, rowspan=2, sticky="NS")
        self.btn_add_list.grid(column=1, row=0, rowspan=2, sticky="NS")

        self.filters_labelframe.grid(column=2, row=0, rowspan=2, sticky="NS")

        self.filters1.grid(row=0, sticky="we")
        self.btn_apply_filter1.grid(row=1, sticky="e")
        self.frame_filter1.grid(column=0, row=0, sticky="NSWE")

        self.filters3.grid(row=0, sticky="we")
        self.btn_apply_filter3.grid(row=1, sticky="e")
        self.frame_filter3.grid(column=2, row=0, sticky="NSWE")

        self.filters2.grid(row=0, sticky="we")
        self.btn_apply_filter2.grid(row=1, sticky="e")
        self.frame_filter2.grid(column=3, row=0, sticky="NSWE")

        self.scale.grid(column=4, row=0, sticky="NSWE")
        self.value_label.grid(column=5, row=0, sticky="NSWE")
        self.ticks_label.grid(column=4, row=1, sticky="NSWE")




if __name__ == "__main__":
    app = App()
    style = ThemedStyle(app)
    style.set_theme("black") #breeze, black, arc, aquativo
    app.title('Visualist')
    app.state('zoomed')


    app.mainloop()