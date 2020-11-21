from tkinter import *
from tkinter import Menu
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk


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

        self.canvas = Canvas(self, width=100, height=100, bg='white')

        """ xscrollcommand=self.scroll_x.set,
        yscrollcommand=self.scroll_y.set)
        self.scroll_x = ttk.Scrollbar(self.canvas, orient=HORIZONTAL)
        self.scroll_y = ttk.Scrollbar(self.canvas, orient=VERTICAL)

        self.scroll_x.config(command=self.canvas.xview)
        self.scroll_y.config(command=self.canvas.yview)"""

        self.toolbar_1 = Canvas(self, width=200, height=90)
        self.toolbar_2 = Canvas(self, width=200, height=90)

        self.frame = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.frame,
                                  anchor=N + W)

        self.canvas.grid(row=2, column=0, columnspan=5, rowspan=5)

        """self.scroll_x.grid( row=3, column=2, sticky="we")
        self.scroll_y.grid( row=2, column=3, sticky="ns")"""

        self.toolbar_1.grid(row=0, column=0, sticky="nswe")
        self.toolbar_2.grid(row=0, column=2, sticky="nse")

        self.label_1 = ttk.Label(self, text="Буфер обмена", font="Arial 9")
        self.label_1.grid(row=1, column=0)

        self.label_2 = ttk.Label(self, text="Буфер обмена", font="Arial 9")
        self.label_2.grid(row=1, column=2)

        def pic_resize(size: tuple, pic: str):
            self.img = Image.open(pic)
            self.img = self.img.resize(size)
            self.img = ImageTk.PhotoImage(self.img)
            return self.img

        self.pic_paste = pic_resize((20, 20), "pic\paste.png")
        self.btn_1 = ttk.Menubutton(self.toolbar_1, text="Вставить", image=self.pic_paste, compound=RIGHT)
        self.btn_1.menu = Menu(self.btn_1)
        self.btn_1["menu"] = self.btn_1.menu
        self.btn_1.menu.add_checkbutton(label="Вставить")
        self.btn_1.menu.add_checkbutton(label="Вставить из")
        self.btn_1.grid(row=0, column=0, rowspan=3, columnspan=2)

        self.pic_scissors = pic_resize((20, 20), "pic\ножницы.jpg")
        self.btn_2 = ttk.Button(self.toolbar_1, text="Вырезать", image=self.pic_scissors, compound=LEFT)
        self.btn_2.grid(row=0, column=2)

        self.pic_copy = pic_resize((20, 20), "pic\copy.jpg")
        self.btn_3 = ttk.Button(self.toolbar_1, text="Копировать", image=self.pic_copy, compound=LEFT)
        self.btn_3.grid(row=1, column=2)

        self.sep = ttk.Separator(self)
        self.sep.grid(row=0, column=1, rowspan=1, sticky='nswe')

        self.btn_4 = ttk.Button(self.toolbar_2)
        self.btn_4.grid(row=0, column=0)

        self.btn_5 = ttk.Button(self.toolbar_2)
        self.btn_5.grid(row=1, column=0)

        self.btn_6 = ttk.Button(self.toolbar_2)
        self.btn_6.grid(row=2, column=0)

        menuBar = MenuBar(self)
        self.config(menu=menuBar)


if __name__ == "__main__":
    app = App()

    style = ThemedStyle(app)
    style.set_theme("black")
    app.mainloop()
