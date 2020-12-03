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
               command=notebook.image_processing.return_image
               ).pack(pady=5)

        # кнопка смены цвета фона
        Button(frame_img,
               text="bg",
               command=lambda: notebook.image_processing.set_bg()
               ).pack(pady=5)

        # выводит на экран информацию о текущем холсте - для отладки
        Button(frame_img,
               text="get info",
               command=lambda: notebook.image_processing.get_info()
               ).pack(pady=5)

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
        frame_filter1.pack(pady=5)

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

        filter_2_percent = Scale(frame_filter2, from_=0, to=200, orient=HORIZONTAL)
        filter_2_percent.set(100)
        filter_2_percent.pack()

        btn_apply_filter2 = Button(frame_filter2,
                                   text="apply filter",
                                   command=lambda
                                   x=variable_filter_2,
                                   y=filter_2_percent:
                                   notebook.image_processing.apply_filter_2(x, y)
                                   )
        btn_apply_filter2.pack()
        frame_filter2.pack(pady=5)

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
        frame_filter3.pack(pady=5)

        # фильтр 4
        Button(frame_img,
               text="try your luck",
               command=lambda: notebook.image_processing.apply_filter_4()
               ).pack(pady=10)

        # кнопки фильтра 5
        frame_filter5 = LabelFrame(frame_img, text='filter 5')
        r_scale_box = Scale(frame_filter5, from_=0, to=200, orient=HORIZONTAL)
        r_scale_box.set(100)
        g_scale_box = Scale(frame_filter5, from_=0, to=200, orient=HORIZONTAL)
        g_scale_box.set(100)
        b_scale_box = Scale(frame_filter5, from_=0, to=200, orient=HORIZONTAL)
        b_scale_box.set(100)
        r_scale_box.pack()
        g_scale_box.pack()
        b_scale_box.pack()

        btn_apply_filter5 = Button(frame_filter5,
                                   text="apply filter",
                                   command=lambda
                                   r=r_scale_box,
                                   g=g_scale_box,
                                   b=b_scale_box:
                                   notebook.image_processing.change_layers(r, g, b)
                                   )
        btn_apply_filter5.pack()
        frame_filter5.pack(pady=5)

        # frame_img.grid(row=0, column=0, sticky="nsew")

        toolbar.add(frame_graphic, text="GRAPHIC")
        colors = ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet')
        thickness_list = sample(range(5, 20), 6)

        btnClear = Button(frame_graphic, text='*отчистить*', command=lambda: notebook.events.event_btnClear())
        btnClear.pack(side=TOP, pady=5)

        btnMove = Button(frame_graphic, text='*подвинуть*',
                         command=lambda ms=core.DEFAULT_MOUSE_SPEED:
                         notebook.events.event_move(mouse_speed=ms))
        btnMove.pack(side=TOP, pady=5)

        btnQuickEraser = Button(frame_graphic, text='*быстрый ластик*',
                                command=notebook.events.event_btnQuickEraser)
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
                                    command=lambda t=core.DEFAULT_THICKNESS, outclr=core.DEFAULT_FIRST_COLOR,
                                                   bgclr=core.DEFAULT_SECOND_COLOR:
                                    notebook.events.event_btnCreateRectangle(thickness=t, bgcolor=bgclr, outcolor=outclr))
        btnCreateRectangle.pack(side=TOP, pady=5)
        # frame_graphic.grid(row=1, column=0, sticky="nsew")

        # для корректного отображения canvas'а
        root.rowconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.update_idletasks()
        root.minsize(root.winfo_width(), root.winfo_height())

        # меню с доступными командами
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=lambda: notebook.image_processing.set_image())
        filemenu.add_command(label="Save", command=lambda: notebook.image_processing.save_image())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        menubar.add_command(label='New canvas', command=notebook.create_new_canvas)


        root.config(menu=menubar)



        notebook.bind("<<NotebookTabChanged>>", notebook.select_curr_tab)

        root.bind('<Control-x>', quit)


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
