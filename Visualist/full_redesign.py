from tkinter import *
from tkinter import Menu
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import tkinter.colorchooser

from graphic_lib import _graphic_core as gcore
from image_lib import _image_core as core


class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)

        fileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="Файл", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Открыть...")
        fileMenu.add_command(label="Новый файл")
        fileMenu.add_command(label="Сохранить...")
        fileMenu.add_command(label="Выйти", underline=1, command=self.quit)

        helpMenu = Menu(self, tearoff=0)
        self.add_cascade(label="Ссылки", underline=0, menu=helpMenu)
        helpMenu.add_command(label="Помощь")
        helpMenu.add_command(label="О программе")

    def quit(self):
        sys.exit(0)

class App(Tk):
    def __init__(self):
        super().__init__()

        ico = Image.open('images/visualist.png')
        ico.thumbnail((64, 64), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)

        def image_resize(size: tuple, pic: str):
            return ImageTk.PhotoImage(Image.open(pic).resize(size))

        self.color_code = ((0.0, 0.0, 0.0), '#b6e2f1')
        def choose_color():
            self.color_code = tkinter.colorchooser.askcolor(title="Цвета")
            print(self.color_code[1])

        # параметры иконок
        self.dir = "blacktheme"

        # параметры стилизации
        self.stock_bg = self.color_code[1]
        self.second_bg = "red"
        self.font = "courier"

        # стили
        self.styler = ttk.Style()
        self.styler.configure("TButton", foreground="black", background=self.stock_bg, relief="flat")
        self.styler.configure("TSeparator", foreground="red", background="red")
        self.styler.configure('Red.TLabelframe.Label', font=(self.font, 12), foreground="black", background=self.stock_bg)
        self.styler.configure("Red.TLabelframe", foreground="red", background=self.stock_bg)

        # меню
        menuBar = MenuBar(self)
        self.config(menu=menuBar)



        # главаный контейнер
        self.frame_main = Frame(self)

        # часть кода Егора для функционала

        self.canvas = gcore.CustomCanvas(self.frame_main,
                                         width=gcore.DEFAULT_CANVAS_W, height=gcore.DEFAULT_CANVAS_H,
                                         bg=gcore.DEFAULT_CANVAS_BG,
                                         )
        self.frame_main.grid(row=0, column=0)
        self.canvas.pack(side=BOTTOM)

        events = gcore.Events(self, gcore.DEFAULT_USED_EVENTS, self.canvas)
        colors = ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet')
        events.event_onCanvas()

        # GUI виджеты
        self.nb = ttk.Notebook(self.frame_main, width=900, height=90)
        self.toolbar_1 = ttk.Frame(self.nb)
        self.toolbar_2 = ttk.Frame(self.nb)
        self.nb.add(self.toolbar_1, text='graphic_lib')
        self.nb.add(self.toolbar_2, text='image_lib')

        # страница 1

        self.im_brush = image_resize((30, 30), f"images/{self.dir}/brush.jpg")
        self.btn_brush = ttk.Button(self.toolbar_1, style="TButton", image=self.im_brush,
                                    command=lambda s=gcore.DEFAULT_BRUSH_SIZE, clr=gcore.DEFAULT_FIRST_COLOR:
                                    events.event_btnBrush(size=s, color=clr, debug_mode=False))

        self.im_fill = image_resize((30, 30), f"images/{self.dir}/fill.jpg")
        self.btn_fill = ttk.Button(self.toolbar_1, style="TButton", image=self.im_fill,
                                   command=lambda c=colors:
                                   events.event_btnFill(color=self.color_code[1]))

        self.im_fasteraser = image_resize((30, 30), f"images/{self.dir}/fasteraser.jpg")
        self.btn_fasteraser = ttk.Button(self.toolbar_1, style="TButton", image=self.im_fasteraser,
                                         command=lambda s=gcore.DEFAULT_ERASER_SIZE:
                                         events.event_btnEraser(size=s))

        self.im_eraser = image_resize((30, 30), f"images/{self.dir}/eraser.jpg")
        self.btn_eraser = ttk.Button(self.toolbar_1, style="TButton", image=self.im_eraser,
                                     command=events.event_btnQuickEraser)

        self.sep_1 = ttk.Separator(self.toolbar_1, style="TSeparator", orient=VERTICAL)

        self.im_color = image_resize((70, 70), f"images/{self.dir}/color.jpg")
        self.btn_colorchoice = ttk.Button(self.toolbar_1, style="TButton", image=self.im_color, command = choose_color)

        self.sep_2 = ttk.Separator(self.toolbar_1, style="TSeparator", orient=VERTICAL)

        self.im_replace = image_resize((30, 30), f"images/{self.dir}/replace.jpg")
        self.btn_replace = ttk.Button(self.toolbar_1, style="TButton", image=self.im_replace,
                                      command=lambda ms=gcore.DEFAULT_MOUSE_SPEED:
                                      events.event_move(mouse_speed=ms))

        self.im_delete = image_resize((30, 30), f"images/{self.dir}/delete.jpg")
        self.btn_delete = ttk.Button(self.toolbar_1, style="TButton", image=self.im_delete, command=events.event_btnClear)

        self.im_undo = image_resize((30, 30), f"images/{self.dir}/undo.jpg")
        self.btn_undo = ttk.Button(self.toolbar_1, style="TButton", image=self.im_undo)

        self.im_redo = image_resize((30, 30), f"images/{self.dir}/redo.jpg")
        self.btn_redo = ttk.Button(self.toolbar_1, style="TButton", image=self.im_redo)

        self.sep_3 = ttk.Separator(self.toolbar_1, style="TSeparator", orient=VERTICAL)

        self.figure_labelframe = ttk.Labelframe(self.toolbar_1, text="Фигуры", style="Red.TLabelframe")

        self.pic_rectangle = image_resize((25, 20), f"images/{self.dir}/rectangle.jpg")
        self.btn_rectangle = ttk.Button(self.figure_labelframe, image=self.pic_rectangle,
                                    command=lambda t=gcore.DEFAULT_THICKNESS, outclr=gcore.DEFAULT_FIRST_COLOR,
                                                   bgclr=gcore.DEFAULT_SECOND_COLOR:
                                    events.event_btnCreateRectangle(thickness=t, bgcolor=bgclr, outcolor=outclr),
                                    style="TButton")

        self.pic_line = image_resize((25, 20), f"images/{self.dir}/line.jpg")
        self.btn_line = ttk.Button(self.figure_labelframe, image=self.pic_line,
                               command=lambda t=gcore.DEFAULT_THICKNESS, clr=gcore.DEFAULT_FIRST_COLOR:
                               events.event_btnCreateLine(thickness=t, color=clr),
                               style="TButton")

        self.pic_ellipsis = image_resize((25, 20), f"images/{self.dir}/ellipsis.jpg")
        self.btn_ellipsis = ttk.Button(self.figure_labelframe, image=self.pic_ellipsis,
                                   command=lambda t=gcore.DEFAULT_THICKNESS, outclr=gcore.DEFAULT_FIRST_COLOR,
                                                  bgclr=gcore.DEFAULT_SECOND_COLOR: events.event_btnCreateOval(
                                       thickness=t, bgcolor=bgclr, outcolor=outclr),
                                   style="TButton")

        self.pic_polygon = image_resize((25, 20), f"images/{self.dir}/polygon.jpg")
        self.btn_polygon = ttk.Button(self.figure_labelframe, image=self.pic_polygon, style="TButton",
                                  command=lambda t=gcore.DEFAULT_THICKNESS, outclr=gcore.DEFAULT_FIRST_COLOR,
                                                 bgclr=gcore.DEFAULT_SECOND_COLOR:
                                  events.event_btnCreatePolygon(thickness=t, bgcolor=bgclr, outcolor=outclr))

        # страница 2

        self.im_return = image_resize((30, 30), f"images/{self.dir}/return.jpg")
        self.btn_return = ttk.Button(self.toolbar_2, image=self.im_return, style="TButton")

        self.im_add_list = image_resize((30, 30), f"images/{self.dir}/add_list.jpg")
        self.btn_add_list = ttk.Button(self.toolbar_2, text="Добавить холст", image=self.im_add_list, compound=LEFT, style="TButton")

        self.filters_labelframe = ttk.Labelframe(self.toolbar_2, text="Фильтры", style="Red.TLabelframe")

        self.frame_filter1 = ttk.Frame(self.filters_labelframe)
        self.variable_filter_1 = StringVar(self.frame_filter1)
        self.variable_filter_1.set(core.DEFAULT_FILTERS_1[0])
        self.filters1 = ttk.OptionMenu(self.frame_filter1,self.variable_filter_1,*core.DEFAULT_FILTERS_1)
        self.btn_apply_filter1 = ttk.Button(self.frame_filter1, text="Применить")

        self.frame_filter3 = ttk.Frame(self.filters_labelframe)
        self.variable_filter_3 = StringVar(self.frame_filter3)
        self.variable_filter_3.set(core.DEFAULT_FILTERS_3[0])
        self.filters3 = ttk.OptionMenu(self.frame_filter3, self.variable_filter_3, *core.DEFAULT_FILTERS_3)
        self.btn_apply_filter3 = ttk.Button(self.frame_filter3, text="Применить")

        self.frame_filter2 = ttk.Frame(self.filters_labelframe)
        self.variable_filter_2 = StringVar(self.frame_filter2)
        self.variable_filter_2.set(core.DEFAULT_FILTERS_2[0])
        self.filters2 = ttk.OptionMenu(self.frame_filter2,self.variable_filter_2,*core.DEFAULT_FILTERS_2)
        self.btn_apply_filter2 = ttk.Button(self.frame_filter2, text="Применить")

        def ttk_slider_callback(value):
            self.value_label.config(text=round(float(value)))

        self.value_label = ttk.Label(self.frame_filter2, text=100)
        self.scale = ttk.Scale(self.frame_filter2, length=150, from_=100, to=500, command=ttk_slider_callback)
        self.ticks_label = ttk.Label(self.frame_filter2, text='100     200     300     400     500')



        # упаковка виджетов
        self.nb.pack(side=TOP, anchor=NW)

        self.btn_brush.grid(column=0, row=0, sticky="NSWE")
        self.btn_fill.grid(column=1, row=0, sticky="NSWE")
        self.btn_fasteraser.grid(column=0, row=1, sticky="NSWE")
        self.btn_eraser.grid(column=1, row=1, sticky="NSWE")

        self.sep_1.grid(row=0, column=2, rowspan=2, sticky="NSWE")

        self.btn_colorchoice.grid(row=0, column=4, rowspan=2, columnspan=2, sticky="NSWE")

        self.sep_2.grid(row=0, column=6, rowspan=2, sticky="NSWE")

        self.btn_replace.grid(row=0, column=7, sticky="NSWE")
        self.btn_delete.grid(row=0, column=8, sticky="NSWE")
        self.btn_undo.grid(row=1, column=7, sticky="NSWE")
        self.btn_redo.grid(row=1, column=8, sticky="NSWE")

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
    app.geometry('900x900')
    app.mainloop()