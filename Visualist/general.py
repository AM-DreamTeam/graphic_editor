from tkinter import *
from tkinter import Menu
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import tkinter.colorchooser

from graphic_lib import _graphic_core as gcore


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

        self.frame_main = Frame(self)

        self.nb = ttk.Notebook(self.frame_main, width=1000, height=90)
        self.toolbar_1 = Canvas(self.nb)
        self.toolbar_2 = Canvas(self.nb)
        self.nb.add(self.toolbar_1, text='Главная')
        self.nb.add(self.toolbar_2, text='Работа с документом')



        self.canvas = gcore.CustomCanvas(self.frame_main, width=gcore.DEFAULT_CANVAS_W, height=gcore.DEFAULT_CANVAS_H,
                                         bg=gcore.DEFAULT_CANVAS_BG)
        events = gcore.Events(self, gcore.DEFAULT_USED_EVENTS, self.canvas)

        self.bind('<Control-x>', quit)
        self.bind('<Control-z>', lambda event: events.event_undo())
        self.bind('<Control-s>', lambda event: print(self.canvas.obj_storage))# не рабоатет пока ни один бинд

        self.frame_main.grid(row=0, column=0)
        self.nb.pack(side=TOP, anchor=NW)
        self.canvas.pack(side=TOP)


        colors = ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet')

        events = gcore.Events(self, gcore.DEFAULT_USED_EVENTS, self.canvas)

        events.event_onCanvas()


        self.label_1 = Label(self.toolbar_1, text="Буфер обмена", font="Arial 9")
        self.label_2 = Label(self.toolbar_1, text="Цвета", font="Arial 9")
        self.label_3 = Label(self.toolbar_1, text="Панель инструментов", font="Arial 9")


        def pic_resize(size: tuple, pic: str):
            self.img = Image.open(pic)
            self.img = self.img.resize(size)
            self.img = ImageTk.PhotoImage(self.img)
            return self.img

        self.color_code = ((0.0, 0.0, 0.0), '#000000')
        def choose_color():
            self.color_code = tkinter.colorchooser.askcolor(title="Цвета")


        self.pic_paste = pic_resize((20, 20), "images/paste.png")
        self.btn_paste = Menubutton(self.toolbar_1, text="Вставить", image=self.pic_paste, compound=RIGHT, width=90,
                                    height=60)
        self.btn_paste.menu = Menu(self.btn_paste)
        self.btn_paste["menu"] = self.btn_paste.menu
        self.btn_paste.menu.add_checkbutton(label="Вставить")
        self.btn_paste.menu.add_checkbutton(label="Вставить из")

        self.pic_scissors = pic_resize((20, 20), "images/ножницы.jpg")
        self.btn_cut = Button(self.toolbar_1, text="Вырезать", image=self.pic_scissors, compound=LEFT, width=90,
                              height=25, relief=GROOVE)

        self.pic_copy = pic_resize((20, 20), "images/copy.jpg")
        self.btn_copy = Button(self.toolbar_1, text="Копировать", image=self.pic_copy, compound=LEFT, width=90, height=25,
                               relief=GROOVE)

        self.sep_1 = ttk.Separator(self.toolbar_1, orient=VERTICAL)

        self.pic_ch = pic_resize((20, 20), "images/choicee.jpg")
        self.btn_colorchoice = Button(self.toolbar_1, text="Выбор цвета", image=self.pic_ch,
                                      command = choose_color, compound=RIGHT, width=90, height=59, relief=GROOVE)


        self.sep_2 = ttk.Separator(self.toolbar_1, orient=VERTICAL)

        self.tool_labelframe = ttk.Labelframe(self.toolbar_1, text="Инструменты", width=90, height=51)

        self.pic_brush = pic_resize((30, 30), "images/brush.jpg")
        self.btn_brush = Button(self.tool_labelframe, image=self.pic_brush,
                                command=lambda s=gcore.DEFAULT_BRUSH_SIZE, clr=gcore.DEFAULT_FIRST_COLOR:
                            events.event_btnBrush(size=s, color=clr, debug_mode=False),
                                width=30, height=20, relief=GROOVE)

        self.pic_fill = pic_resize((30, 30), "images/fill.jpg")
        self.btn_fill = Button(self.tool_labelframe, image=self.pic_fill,
                               command=lambda c=colors:
                            events.event_btnFill(color=self.color_code[1]),
                               width=30, height=20, relief=GROOVE)

        self.pic_eraser = pic_resize((30, 30), "images/eraser.jpg")
        self.btn_eraser = Button(self.tool_labelframe, image=self.pic_eraser,
                                 command=events.event_btnClear,
                                 width=30, height=20, relief=GROOVE)

        self.btn_8 = Button(self.tool_labelframe, image=self.pic_eraser, width=30, height=20, relief=GROOVE)
        self.btn_9 = Button(self.tool_labelframe, image=self.pic_eraser, width=30, height=20, relief=GROOVE)
        self.btn_10 = Button(self.tool_labelframe, image=self.pic_eraser, width=30, height=20, relief=GROOVE)

        self.figure_labelframe = ttk.Labelframe(self.toolbar_1, text="Фигуры", width=90, height=51)

        self.pic_rectangle = pic_resize((30, 30), "images/rectangle.jpg")
        self.btn_rectangle = Button(self.figure_labelframe, image=self.pic_rectangle,
                                    command=lambda t=gcore.DEFAULT_THICKNESS, outclr=gcore.DEFAULT_FIRST_COLOR,
                                            bgclr=gcore.DEFAULT_SECOND_COLOR:
                             events.event_btnCreateRectangle(thickness=t, bgcolor=bgclr, outcolor=outclr),
                                    width=30, height=20, relief=GROOVE)

        self.pic_line = pic_resize((30, 30), "images/line.jpg")
        self.btn_line = Button(self.figure_labelframe, image=self.pic_line,
                               command=lambda t=gcore.DEFAULT_THICKNESS, clr=gcore.DEFAULT_FIRST_COLOR:
                             events.event_btnCreateLine(thickness=t, color=clr),
                               width=30, height=20, relief=GROOVE)

        self.pic_ellipsis = pic_resize((30, 30), "images/ellipsis.jpg")
        self.btn_ellipsis = Button(self.figure_labelframe, image=self.pic_ellipsis,
                                   command=lambda t=gcore.DEFAULT_THICKNESS, outclr=gcore.DEFAULT_FIRST_COLOR,
                             bgclr=gcore.DEFAULT_SECOND_COLOR:events.event_btnCreateOval(thickness=t, bgcolor=bgclr, outcolor=outclr),
                                   width=30, height=20, relief=GROOVE)

        self.pic_polygon = pic_resize((30, 30), "images/polygon.jpg")
        self.btn_polygon = Button(self.figure_labelframe, image=self.pic_polygon,
                                  command=lambda t=gcore.DEFAULT_THICKNESS, outclr=gcore.DEFAULT_FIRST_COLOR,
                                            bgclr=gcore.DEFAULT_SECOND_COLOR:
                             events.event_btnCreatePolygon(thickness=t, bgcolor=bgclr, outcolor=outclr),
                                  width=30, height=20, relief=GROOVE)




        self.btn_paste.grid(row=0, column=0, rowspan=3, columnspan=2)
        self.btn_cut.grid(row=0, column=2, sticky="NS")
        self.btn_copy.grid(row=1, column=2, sticky="NS")
        self.label_1.grid(row=3, column=0, columnspan=3)


        self.sep_1.grid(row=0, column=3, rowspan=4,  sticky="NSWE")


        self.btn_colorchoice.grid(row=0, column=4, rowspan=3, columnspan=2)
        self.label_2.grid(row=3, column=4, columnspan=2)


        self.sep_2.grid(row=0, column=6, rowspan=4, sticky="NSWE")

        self.tool_labelframe.grid(row=0, column=7, rowspan=3, sticky="NSWE")
        self.label_3.grid(row=3, column=7, columnspan=5)
        self.btn_brush.grid(row=0, column=0)
        self.btn_fill.grid(row=0, column=1)
        self.btn_eraser.grid(row=0, column=2)
        self.btn_8.grid(row=1, column=0)
        self.btn_9.grid(row=1, column=1)
        self.btn_10.grid(row=1, column=2)

        self.figure_labelframe.grid(row=0, column=11, rowspan=3, sticky="NS")
        self.btn_rectangle.grid(row=0, column=0)
        self.btn_line.grid(row=0, column=1)
        self.btn_ellipsis.grid(row=0, column=2)
        self.btn_polygon.grid(row=1, column=0)



        menuBar = MenuBar(self)
        self.config(menu=menuBar)


if __name__ == "__main__":
    app = App()
    app.title('Visualist')
    app.resizable(False, False) # бага с изменением размера окна
    app.geometry('700x700')

    app.mainloop()
