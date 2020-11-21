from tkinter import *
from tkinter import Menu
import tkinter.ttk as ttk
from PIL import Image, ImageTk

from random import choice
from graphic_lib import _graphic_core as gcore


class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)

        fileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Open...")
        fileMenu.add_command(label="New file")
        fileMenu.add_command(label="Save...")
        fileMenu.add_command(label="Exit", underline=1, command=self.quit)

        helpMenu = Menu(self, tearoff=0)
        self.add_cascade(label="Reference", underline=0, menu=helpMenu)
        helpMenu.add_command(label="Help")
        helpMenu.add_command(label="About")

    def quit(self):
        sys.exit(0)


class App(Tk):
    def __init__(self):
        super().__init__()

        ico = Image.open('pic/visualist.png')
        ico.thumbnail((64, 64), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(ico)

        self.wm_iconphoto(False, photo)

        self.frame_main = Frame(self)

        self.toolbar_1 = Canvas(self.frame_main)

        self.canvas = gcore.CustomCanvas(self.frame_main, width=gcore.DEFAULT_CANVAS_W, height=gcore.DEFAULT_CANVAS_H,
                                         bg=gcore.DEFAULT_CANVAS_BG)

        self.frame_main.grid(row=0, column=0)
        self.toolbar_1.pack(side=TOP, anchor=NW)
        self.canvas.pack(side=TOP)


        colors = ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet')

        events = gcore.Events(self, gcore.DEFAULT_USED_EVENTS, self.canvas)




        self.label_1 = Label(self.toolbar_1, text="Буфер обмена", font="Arial 9")
        self.label_2 = Label(self.toolbar_1, text="Цвета", font="Arial 9")
        self.label_3 = Label(self.toolbar_1, text="Панель инструментов", font="Arial 9")


        def pic_resize(size: tuple, pic: str):
            self.img = Image.open(pic)
            self.img = self.img.resize(size)
            self.img = ImageTk.PhotoImage(self.img)
            return self.img



        self.pic_paste = pic_resize((20, 20), "pic/paste.png")
        self.btn_1 = Menubutton(self.toolbar_1, text="Вставить", image=self.pic_paste, compound=RIGHT, width=90,
                                height=60)
        self.btn_1.menu = Menu(self.btn_1)
        self.btn_1["menu"] = self.btn_1.menu
        self.btn_1.menu.add_checkbutton(label="Вставить")
        self.btn_1.menu.add_checkbutton(label="Вставить из")

        self.pic_scissors = pic_resize((20, 20), "pic/ножницы.jpg")
        self.btn_2 = Button(self.toolbar_1, text="Вырезать", image=self.pic_scissors, compound=LEFT, width=90,
                            height=25, relief=GROOVE)

        self.pic_copy = pic_resize((20, 20), "pic/copy.jpg")
        self.btn_3 = Button(self.toolbar_1, text="Копировать", image=self.pic_copy, compound=LEFT, width=90, height=25,
                            relief=GROOVE)

        self.sep_1 = ttk.Separator(self.toolbar_1, orient=VERTICAL)

        self.pic_ch = pic_resize((20, 20), "pic/choicee.jpg")
        self.btn_4 = Button(self.toolbar_1, text="Выбор цвета", image=self.pic_ch, compound=RIGHT, width=90, height=57, relief=GROOVE)


        self.sep_2 = ttk.Separator(self.toolbar_1, orient=VERTICAL)

        self.tool_labelframe = ttk.Labelframe(self.toolbar_1, text="Инструменты", width=90, height=51)

        self.pic_brush = pic_resize((30, 30), "pic/brush.jpg")
        self.btn_5 = Button(self.tool_labelframe, image=self.pic_brush,
                            command=lambda s=gcore.DEFAULT_BRUSH_SIZE, clr=gcore.DEFAULT_FIRST_COLOR:
                            events.event_btnBrush(size=s, color=clr, debug_mode=False),
                            width=30, height=20, relief=GROOVE)

        self.pic_fill = pic_resize((30, 30), "pic/fill.jpg")
        self.btn_6 = Button(self.tool_labelframe, image=self.pic_fill,
                            command=lambda c=colors:events.event_btnFill(color=choice(c)),
                            width=30, height=20, relief=GROOVE)

        self.pic_eraser = pic_resize((30, 30), "pic/eraser.jpg")
        self.btn_7 = Button(self.tool_labelframe, image=self.pic_eraser,
                            command=events.event_btnClear,
                            width=30, height=20, relief=GROOVE)

        self.btn_8 = Button(self.tool_labelframe, image=self.pic_eraser, width=30, height=20, relief=GROOVE)
        self.btn_9 = Button(self.tool_labelframe, image=self.pic_eraser, width=30, height=20, relief=GROOVE)
        self.btn_10 = Button(self.tool_labelframe, image=self.pic_eraser, width=30, height=20, relief=GROOVE)

        self.figure_labelframe = ttk.Labelframe(self.toolbar_1, text="Фигуры", width=90, height=51)

        self.pic_rectangle = pic_resize((30, 30), "pic/rectangle.jpg")
        self.btn_11 = Button(self.figure_labelframe, image=self.pic_rectangle,
                             command=lambda t=gcore.DEFAULT_THICKNESS, outclr=gcore.DEFAULT_FIRST_COLOR,
                                            bgclr=gcore.DEFAULT_SECOND_COLOR:
                             events.event_btnCreateRectangle(thickness=t, bgcolor=bgclr, outcolor=outclr),
                             width=30, height=20, relief=GROOVE)

        self.pic_line = pic_resize((30, 30), "pic/line.jpg")
        self.btn_12 = Button(self.figure_labelframe, image=self.pic_line,
                             command=lambda t=gcore.DEFAULT_THICKNESS, clr=gcore.DEFAULT_FIRST_COLOR:
                             events.event_btnCreateLine(thickness=t, color=clr),
                             width=30, height=20, relief=GROOVE)

        self.pic_ellipsis = pic_resize((30, 30), "pic/ellipsis.jpg")
        self.btn_13 = Button(self.figure_labelframe, image=self.pic_ellipsis,
                             command=lambda t=gcore.DEFAULT_THICKNESS, outclr=gcore.DEFAULT_FIRST_COLOR,
                             bgclr=gcore.DEFAULT_SECOND_COLOR:events.event_btnCreateOval(thickness=t, bgcolor=bgclr, outcolor=outclr),
                             width=30, height=20, relief=GROOVE)




        self.btn_1.grid(row=0, column=0, rowspan=3, columnspan=2)
        self.btn_2.grid(row=0, column=2, sticky="NS")
        self.btn_3.grid(row=1, column=2, sticky="NS")
        self.label_1.grid(row=3, column=0, columnspan=3)


        self.sep_1.grid(row=0, column=3, rowspan=4,  sticky="NSWE")


        self.btn_4.grid(row=0, column=4, rowspan=3, columnspan=2, sticky="NSWE")
        self.label_2.grid(row=3, column=4, columnspan=2)


        self.sep_2.grid(row=0, column=6, rowspan=4, sticky="NSWE")

        self.tool_labelframe.grid(row=0, column=7, rowspan=3, sticky="NSWE")
        self.label_3.grid(row=3, column=7, columnspan=5)
        self.btn_5.grid(row=0, column=0)
        self.btn_6.grid(row=0, column=1)
        self.btn_7.grid(row=0, column=2)
        self.btn_8.grid(row=1, column=0)
        self.btn_9.grid(row=1, column=1)
        self.btn_10.grid(row=1, column=2)

        self.figure_labelframe.grid(row=0, column=11, rowspan=3, sticky="NS")
        self.btn_11.grid(row=0, column=0)
        self.btn_12.grid(row=0, column=1)
        self.btn_13.grid(row=0, column=2)



        menuBar = MenuBar(self)
        self.config(menu=menuBar)


if __name__ == "__main__":
    app = App()
    app.title('Visualist')
    app.geometry('700x700')
    app.bind('<Control-z>', lambda event: gcore.Events.event_undo())

    app.mainloop()
