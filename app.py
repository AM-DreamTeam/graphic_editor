from tkinter import *
from core import core
from random import choice, sample
from tkinter.ttk import Notebook


class App:

    def __init__(self, root):
        root.geometry('1000x600')
        # root.state('zoomed')

        toolbar = Notebook(root)
        # фрейм для кпопок
        frame_img = LabelFrame(toolbar, text='Изображения')
        frame_graphic = LabelFrame(toolbar, text='Графические примитивы')
        toolbar.grid(row=0, column=0, rowspan=2, sticky="nswe")

        # инициализуем Notebook
        notebook = core.CustomNotebook(root)
        notebook.grid(row=0, column=1, rowspan=2, sticky="nswe")

        toolbar.add(frame_img, text="IMAGE")
        # кнопка возврата предыдущего изображения
        Button(frame_img,
               text="return image",
               command=lambda: notebook.image_processing.return_image()
               ).pack()

        # кнопки фильтра 1

        # создаем выпадающее меню
        frame_filter1 = LabelFrame(frame_img, text="filter 1")
        variable_filter_1 = StringVar(frame_filter1)
        variable_filter_1.set(core.DEFAULT_FILTERS_1[0])
        filters1 = OptionMenu(frame_filter1,
                              variable_filter_1,
                              *core.DEFAULT_FILTERS_1)
        filters1.grid(row=0, sticky="we")

        # применяет тот фильтр, который выбран в меню выше
        btn_apply_filter1 = Button(frame_filter1,
                                   text="apply filter",
                                   command=lambda x=variable_filter_1:
                                   notebook.image_processing.apply_filter_1(x)
                                   )
        btn_apply_filter1.grid(row=1, sticky="e")
        frame_filter1.pack()

        # кнопки фильтра 2

        # все тоже самое, только еще есть поле Entry, в которое вводится значение коэффициента,
        # при котором происходит фильтрация
        frame_filter2 = LabelFrame(frame_img, text='filter 2')
        variable_filter_2 = StringVar(frame_filter2)
        variable_filter_2.set(core.DEFAULT_FILTERS_2[0])
        filters2 = OptionMenu(frame_filter2,
                              variable_filter_2,
                              *core.DEFAULT_FILTERS_2
                              )
        filters2.pack()

        self.filter_2_percent = Scale(frame_filter2, from_=0, to=200, orient=HORIZONTAL)
        self.filter_2_percent.set(100)
        self.filter_2_percent.pack()

        self.filter_2_percent.bind("<B1-Motion>", lambda
                                   event,
                                   filter=variable_filter_2,
                                   scale=self.filter_2_percent:
                                   notebook.image_processing.apply_filter_2(f=filter, per=scale, event=event))

        Button(frame_filter2,
               text='Apply',
               command=
               lambda : [notebook.image_processing.append_image(), self.reset_scales()]
               ).pack()
        frame_filter2.pack()

        # кнопки фильтра 3
        frame_filter3 = LabelFrame(frame_img, text='filter 3')
        variable_filter_3 = StringVar(frame_filter1)
        variable_filter_3.set(core.DEFAULT_FILTERS_3[0])
        filters3 = OptionMenu(frame_filter3,
                              variable_filter_3,
                              *core.DEFAULT_FILTERS_3
                              )
        filters3.grid(row=0, column=0, columnspan=2, sticky="we")

        btn_apply_filter3 = Button(frame_filter3,
                                   text="apply filter",
                                   command=lambda x=variable_filter_3:
                                   notebook.image_processing.apply_filter_3(x)
                                   )
        btn_apply_filter3.grid(row=1, column=0, columnspan=2, sticky="e")
        frame_filter3.pack()

        # кнопки фильтра 4
        frame_filter4 = LabelFrame(frame_img, text='filter 4')
        self.r_scale_box = Scale(frame_filter4, from_=0, to=200, orient=HORIZONTAL)
        self.r_scale_box.set(100)
        self.g_scale_box = Scale(frame_filter4, from_=0, to=200, orient=HORIZONTAL)
        self.g_scale_box.set(100)
        self.b_scale_box = Scale(frame_filter4, from_=0, to=200, orient=HORIZONTAL)
        self.b_scale_box.set(100)
        self.r_scale_box.pack()
        self.g_scale_box.pack()
        self.b_scale_box.pack()

        self.r_scale_box.bind("<B1-Motion>",
                              lambda
                              event,
                              r=self.r_scale_box,
                              g=self.g_scale_box,
                              b=self.b_scale_box:
                               notebook.image_processing.change_layers(red=r, green=g, blue=b, event=event))
        self.g_scale_box.bind("<B1-Motion>", lambda
                              event,
                              r=self.r_scale_box,
                              g=self.g_scale_box,
                              b=self.b_scale_box:
                              notebook.image_processing.change_layers(red=r, green=g, blue=b, event=event))
        self.b_scale_box.bind("<B1-Motion>", lambda
                              event,
                              r=self.r_scale_box,
                              g=self.g_scale_box,
                              b=self.b_scale_box:
                              notebook.image_processing.change_layers(red=r, green=g, blue=b, event=event))

        Button(frame_filter4,
               text='Apply',
               command=
               lambda: [notebook.image_processing.append_image(), self.reset_scales()]
               ).pack()
        frame_filter4.pack()

        # фильтр 5
        frame_filter5 = LabelFrame(frame_img, text='filter 4')
        Button(frame_filter5,
               text="mix layers",
               command=lambda: notebook.image_processing.apply_filter_4()
               ).grid(column=0, row=0)

        Button(frame_filter5,
               text="normalize",
               command=lambda: notebook.image_processing.normalize_image()
               ).grid(column=1, row=0)
        frame_filter5.pack()

        # отражение
        frame_filter6 = LabelFrame(frame_img, text='reflect')
        variable_filter_6 = StringVar(frame_filter6)
        variable_filter_6.set('horizontal')
        filters6 = OptionMenu(frame_filter6,
                              variable_filter_6,
                              "horizontal",
                              'vertical'
                              )
        filters6.pack()

        btn_apply_filter6 = Button(frame_filter6,
                                   text="apply filter",
                                   command=lambda x=variable_filter_6:
                                   notebook.image_processing.reflect_image(x)
                                   )
        btn_apply_filter6.pack()
        frame_filter6.pack()

        # отражение
        frame_filter6 = LabelFrame(frame_img, text='reflect')
        variable_filter_6 = StringVar(frame_filter6)
        variable_filter_6.set('horizontal')
        filters6 = OptionMenu(frame_filter6,
                              variable_filter_6,
                              "horizontal",
                              'vertical'
                              )
        filters6.pack()

        btn_apply_filter6 = Button(frame_filter6,
                                   text="apply filter",
                                   command=lambda x=variable_filter_6:
                                   notebook.image_processing.reflect_image(x)
                                   )
        btn_apply_filter6.pack()
        frame_filter6.pack()

        # отражение
        frame_filter7 = LabelFrame(frame_img, text='reflect')
        variable_filter_7 = StringVar(frame_filter6)
        variable_filter_7.set('90')
        filters7 = OptionMenu(frame_filter7,
                              variable_filter_7,
                              "90",
                              '-90'
                              )
        filters7.grid(column=0, row=0)

        btn_apply_filter7 = Button(frame_filter7,
                                   text="apply filter",
                                   command=lambda x=variable_filter_7:
                                   notebook.image_processing.rotate_image(x)
                                   )
        btn_apply_filter7.grid(column=1, row=0)
        frame_filter7.pack()

        # frame_img.grid(row=0, column=0, sticky="nsew")

        toolbar.add(frame_graphic, text="GRAPHIC")
        colors = ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet')
        thickness_list = sample(range(5, 20), 6)

        btnClear = Button(frame_graphic, text='*отчистить*', command=lambda: notebook.events.event_btnClear())
        btnClear.pack(side=TOP, pady=5)

        btnMove = Button(frame_graphic, text='*подвинуть*',
                         command=lambda: notebook.events.event_move())
        btnMove.pack(side=TOP, pady=5)

        btnQuickEraser = Button(frame_graphic, text='*быстрый ластик*',
                                command=lambda: notebook.events.event_btnQuickEraser())
        btnQuickEraser.pack(side=TOP, pady=5)

        btnBrush = Button(frame_graphic, text='*кисть*',
                          command=lambda s=core.DEFAULT_BRUSH_SIZE, clr=core.DEFAULT_FIRST_COLOR:
                          notebook.events.event_btnBrush(size=s, color=clr, debug_mode=False))
        btnBrush.pack(side=TOP, pady=5)

        btnFill = Button(frame_graphic, text='*заливка*',
                         command=lambda c=colors:
                         notebook.events.event_btnFill(color=choice(c)))
        btnFill.pack(side=TOP, pady=5)

        btnOutlineColor = Button(frame_graphic, text='*обводка*',
                                 command=lambda c=colors:
                                 notebook.events.event_btnOutlineColor(color=choice(colors)))
        btnOutlineColor.pack()

        btnThickness = Button(frame_graphic, text='*толщина*',
                              command=lambda t=thickness_list: notebook.events.event_btnThickness(thickness=choice(t)))
        btnThickness.pack(side=TOP, pady=5)

        btnCreateLine = Button(frame_graphic, text='*линия*',
                               command=lambda t=core.DEFAULT_THICKNESS, clr=core.DEFAULT_FIRST_COLOR:
                               notebook.events.event_btnCreateLine(thickness=t, color=clr))
        btnCreateLine.pack(side=TOP, pady=5)

        btnCreateVector = Button(frame_graphic, text='*вектор*',
                                 command=lambda t=core.DEFAULT_THICKNESS, clr=core.DEFAULT_FIRST_COLOR:
                                 notebook.events.event_btnCreateVector(thickness=t, color=clr))
        btnCreateVector.pack(side=TOP, pady=5)

        btnCreateCoordinatePlane = Button(frame_graphic, text='*плоскость*',
                                          command=lambda: notebook.events.event_btnCreateCoordinatePlane())
        btnCreateCoordinatePlane.pack(side=TOP, pady=5)

        btnCreatePolygon = Button(frame_graphic, text='*многоугольник*',
                                  command=lambda t=core.DEFAULT_THICKNESS, outclr=core.DEFAULT_FIRST_COLOR,
                                                 bgclr=core.DEFAULT_SECOND_COLOR:
                                  notebook.events.event_btnCreatePolygon(thickness=t, bgcolor=bgclr, outcolor=outclr))
        btnCreatePolygon.pack(side=TOP, pady=5)

        btnCreateOval = Button(frame_graphic, text='*эллипс*',
                               command=lambda t=core.DEFAULT_THICKNESS, outclr=core.DEFAULT_FIRST_COLOR,
                                              bgclr=core.DEFAULT_SECOND_COLOR:
                               notebook.events.event_btnCreateOval(thickness=t, bgcolor=bgclr, outcolor=outclr))
        btnCreateOval.pack(side=TOP, pady=5)

        btnCreateRectangle = Button(frame_graphic, text='*прямоугольник*',
                                    command=lambda
                                    t=core.DEFAULT_THICKNESS,
                                    outclr=core.DEFAULT_FIRST_COLOR,
                                    bgclr=core.DEFAULT_SECOND_COLOR:
                                    notebook.events.event_btnCreateRectangle(thickness=t, bgcolor=bgclr, outcolor=outclr))
        btnCreateRectangle.pack(side=TOP, pady=5)

        btnCreateText = Button(frame_graphic, text='*текст*', command=lambda: notebook.events.event_btnCreateText())
        btnCreateText.pack(side=TOP, pady=5)

        # для корректного отображения canvas'а
        root.rowconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.update_idletasks()
        root.minsize(root.winfo_width(), root.winfo_height())

        # меню с доступными командами
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=-2)
        filemenu.add_command(label="Open", command=lambda: notebook.image_processing.set_image())
        filemenu.add_command(label="Save", command=lambda: notebook.image_processing.save_image())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        menubar.add_command(label='New canvas', command=notebook.create_new_canvas)

        menubar.add_command(label='Info', command=lambda: notebook.image_processing.get_info())

        root.config(menu=menubar)

        notebook.bind("<<NotebookTabChanged>>", lambda _: [notebook.select_curr_tab(_), self.reset_scales(_)])

        root.bind('<Control-x>', quit)

    def reset_scales(self, _=None):
        """
            Сбрасывает значения Scale до 100 при смене вкладки
        """
        self.filter_2_percent.set(100)
        self.r_scale_box.set(100)
        self.g_scale_box.set(100)
        self.b_scale_box.set(100)


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
