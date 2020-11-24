from tkinter import *
from image_lib import core





class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        #self.state('zoomed')


        #фрейм для кпопок
        self.frame_btn = Frame(self)


        #scrollbar'ы для canvas
        self.scroll_x = Scrollbar(self, orient=HORIZONTAL)
        self.scroll_y = Scrollbar(self, orient=VERTICAL)


        self.canvas = Canvas(self, width=800, height=600,
                                xscrollcommand=self.scroll_x.set,
                                yscrollcommand=self.scroll_y.set,
                                bg='#E0FFFF')
        self.scroll_x.config(command=self.canvas.xview)
        self.scroll_y.config(command=self.canvas.yview)


        #подключение модуля обработки фото
        self.image_processing = core.Img(self.canvas)


        Button(self.frame_btn, text="return image", command=self.image_processing.return_image).pack(pady=10)

        #кнопки фильтра 1
        self.frame_filter1 = Frame(self.frame_btn)
        self.variable_filter_1 = StringVar(self.frame_filter1)
        self.variable_filter_1.set(core.DEFAULT_FILTERS_1[0])
        self.filters1 = OptionMenu(self.frame_filter1, self.variable_filter_1, *core.DEFAULT_FILTERS_1)
        self.filters1.grid(row=0, sticky="we")


        btnApplyFilter1 = Button(self.frame_filter1, text="apply filter", command=lambda x=self.variable_filter_1: self.image_processing.apply_filter_1(x))
        btnApplyFilter1.grid(row=1, sticky="e")
        self.frame_filter1.pack(pady=10)


        #кнопки фильтра 2
        self.frame_filter2 = Frame(self.frame_btn)
        self.variable_filter_2 = StringVar(self.frame_filter2)
        self.variable_filter_2.set(core.DEFAULT_FILTERS_2[0])
        self.filters2 = OptionMenu(self.frame_filter2, self.variable_filter_2, *core.DEFAULT_FILTERS_2)
        self.filters2.grid(row=0, sticky="we", columnspan=2)

        self.variable_filter_2_percent = StringVar(self.frame_filter2)
        self.variable_filter_2_percent.set(100)
        self.entry_filter2 = Entry(self.frame_filter2, textvariable=self.variable_filter_2_percent)
        self.entry_filter2.grid(row=1, column=0)
        Label(self.frame_filter2, text="%").grid(row=1, column=1)

        btnApplyFilter2 = Button(self.frame_filter2, text="apply filter", command=lambda x=self.variable_filter_2, y=self.variable_filter_2_percent: self.image_processing.apply_filter_2(x, y))
        btnApplyFilter2.grid(row=2, column=0, columnspan=2, sticky="we")
        self.frame_filter2.pack(pady=10)


        #кнопки фильтра 3
        self.frame_filter3 = Frame(self.frame_btn)
        self.variable_filter_3 = StringVar(self.frame_filter1)
        self.variable_filter_3.set(core.DEFAULT_FILTERS_3[0])
        self.filters3 = OptionMenu(self.frame_filter3, self.variable_filter_3, *core.DEFAULT_FILTERS_3)
        self.filters3.grid(row=0, column=0, columnspan=2, sticky="we")


        btnApplyFilter3 = Button(self.frame_filter3, text="apply filter", command=lambda x=self.variable_filter_3: self.image_processing.apply_filter_3(x))
        btnApplyFilter3.grid(row=1, column=0, columnspan=2, sticky="e")
        self.frame_filter3.pack(pady=10)



        #фильтр 4
        Button(self.frame_btn, text="try your luck", command=self.image_processing.apply_filter_4).pack(pady=10)

        self.frame_btn.grid(row=0, column=0, rowspan=2, sticky="nsew")


        #frame для canvas'a, чтобы scrollbar корректно работал
        #подробнее тут - https://pythonru.com/uroki/sozdanie-skrollbarov-tkinter-6
        self.cnv_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.cnv_frame,
                                  anchor=N + W)

        self.canvas.grid(row=0, column=1, sticky="nswe")
        self.scroll_x.grid(row=1, column=1, sticky="we")
        self.scroll_y.grid(row=0, column=2, sticky="ns")


        #для корректного отображения canvas'а
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.bind("<Configure>", self.resize)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())




        #меню с доступными командами
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.image_processing.set_image)
        filemenu.add_command(label="Save", command=self.image_processing.save_image)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)


    def resize(self, event):
        """
        Метод resize обрабатывает событие изменения размера окна и обновляет параметр scrollregion,
        определяющий область Canvas, которую можно скроллить.
        """
        region = self.canvas.bbox(ALL)
        self.canvas.configure(scrollregion=region)





if __name__ == "__main__":
    app = App()
    app.mainloop()
