from tkinter import *
from tkinter.ttk import Notebook
from image_lib import _image_core as imcore
from graphic_lib import _graphic_core as gcore
from random import choice, sample


class App:
    def __init__(self, root):
        root.geometry('800x600')
        # root.state('zoomed')

        # фрейм для кпопок
        nb = Notebook(root)


        frame_img = Frame(nb)
        frame_graphic = Frame(nb)
        nb.grid(row=0,
                column=0, rowspan=2, sticky="nswe")
        nb.add(frame_img, text="IMAGE")


        # инициализуем Notebook
        notebook = imcore.CustomNotebook(root)
        notebook.grid(row=0, column=1, rowspan=2, sticky="nswe")

        # кнопка возврата предыдущего изображения
        Button(frame_img,
               text="return image",
               command=lambda: notebook.image_processing.return_image()
               ).pack(pady=10)

        # кнопка создания новой вкладки
        Button(frame_img,
               text="new canvas",
               command=notebook.create_new_canvas
               ).pack(pady=10)

        # кнопка смены увета фона
        Button(frame_img,
               text="bg",
               command=lambda: notebook.image_processing.set_bg()
               ).pack(pady=10)

        # выводит на экран информацию о текущем холсте - для отладки
        Button(frame_img,
               text="get info",
               command=lambda: notebook.image_processing.get_info()
               ).pack(pady=10)

        # кнопки фильтра 1

        # создаем выпадающее меню
        frame_filter1 = Frame(frame_img)
        variable_filter_1 = StringVar(frame_filter1)
        variable_filter_1.set(imcore.DEFAULT_FILTERS_1[0])
        filters1 = OptionMenu(frame_filter1,
                              variable_filter_1,
                              *imcore.DEFAULT_FILTERS_1)
        filters1.grid(row=0, sticky="we")

        # применяет тот фильтр, который выбран в меню выше
        btn_apply_filter1 = Button(frame_filter1,
                                   text="apply filter",
                                   command=lambda x=variable_filter_1:
                                   notebook.image_processing.apply_filter_1(x)
                                   )
        btn_apply_filter1.grid(row=1, sticky="e")
        frame_filter1.pack(pady=10)

        # кнопки фильтра 2

        # все тоже самое, только еще есть поле Entry, в которое вводится значение коэффициента,
        # при котором происходит фильтрация
        frame_filter2 = Frame(frame_img)
        variable_filter_2 = StringVar(frame_filter2)
        variable_filter_2.set(imcore.DEFAULT_FILTERS_2[0])
        filters2 = OptionMenu(frame_filter2,
                              variable_filter_2,
                              *imcore.DEFAULT_FILTERS_2
                              )
        filters2.grid(row=0, sticky="we", columnspan=2)

        variable_filter_2_percent = StringVar(frame_filter2)
        variable_filter_2_percent.set(100)
        entry_filter2 = Entry(frame_filter2,
                              textvariable=variable_filter_2_percent
                              )
        entry_filter2.grid(row=1, column=0)
        Label(frame_filter2, text="%").grid(row=1, column=1)

        btn_apply_filter2 = Button(frame_filter2,
                                   text="apply filter",
                                   command=lambda
                                   x=variable_filter_2,
                                   y=variable_filter_2_percent:
                                   notebook.image_processing.apply_filter_2(x, y)
                                   )
        btn_apply_filter2.grid(row=2, column=0, columnspan=2, sticky="we")
        frame_filter2.pack(pady=10)

        # кнопки фильтра 3
        frame_filter3 = Frame(frame_img)
        variable_filter_3 = StringVar(frame_filter1)
        variable_filter_3.set(imcore.DEFAULT_FILTERS_3[0])
        filters3 = OptionMenu(frame_filter3,
                              variable_filter_3,
                              *imcore.DEFAULT_FILTERS_3
                              )
        filters3.grid(row=0, column=0, columnspan=2, sticky="we")

        btn_apply_filter3 = Button(frame_filter3,
                                   text="apply filter",
                                   command=lambda x=variable_filter_3:
                                   notebook.image_processing.apply_filter_3(x)
                                   )
        btn_apply_filter3.grid(row=1, column=0, columnspan=2, sticky="e")
        frame_filter3.pack(pady=10)

        # фильтр 4
        Button(frame_img,
               text="try your luck",
               command=lambda: notebook.image_processing.apply_filter_4()
               ).pack(pady=10)

        # frame_img.grid(sticky="nsew")

        nb.add(frame_graphic, text="GRAPHIC")
        colors = ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet')
        thickness_list = sample(range(5, 20), 6)

        btnClear = Button(frame_graphic, text='*отчистить*', command=lambda: notebook.events.event_btnClear())
        btnClear.pack(side=TOP, pady=5)

        btnMove = Button(frame_graphic, text='*подвинуть*',
                         command=lambda ms=imcore.DEFAULT_MOUSE_SPEED:
                         notebook.events.event_move(mouse_speed=ms))
        btnMove.pack(side=TOP, pady=5)

        btnQuickEraser = Button(frame_graphic, text='*быстрый ластик*',
                                command=notebook.events.event_btnQuickEraser)
        btnQuickEraser.pack(side=TOP, pady=5)

        btnBrush = Button(frame_graphic, text='*кисть*',
                          command=lambda s=imcore.DEFAULT_BRUSH_SIZE, clr=imcore.DEFAULT_FIRST_COLOR:
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
                               command=lambda t=imcore.DEFAULT_THICKNESS, clr=imcore.DEFAULT_FIRST_COLOR:
                               notebook.events.event_btnCreateLine(thickness=t, color=clr))
        btnCreateLine.pack(side=TOP, pady=5)

        btnCreatePolygon = Button(frame_graphic, text='*многоугольник*',
                                  command=lambda t=imcore.DEFAULT_THICKNESS, outclr=imcore.DEFAULT_FIRST_COLOR,
                                                 bgclr=imcore.DEFAULT_SECOND_COLOR:
                                  notebook.events.event_btnCreatePolygon(thickness=t, bgcolor=bgclr, outcolor=outclr))
        btnCreatePolygon.pack(side=TOP, pady=5)

        btnCreateOval = Button(frame_graphic, text='*эллипс*',
                               command=lambda t=imcore.DEFAULT_THICKNESS, outclr=imcore.DEFAULT_FIRST_COLOR,
                                              bgclr=imcore.DEFAULT_SECOND_COLOR:
                               notebook.events.event_btnCreateOval(thickness=t, bgcolor=bgclr, outcolor=outclr))
        btnCreateOval.pack(side=TOP, pady=5)

        btnCreateRectangle = Button(frame_graphic, text='*прямоугольник*',
                                    command=lambda t=imcore.DEFAULT_THICKNESS, outclr=imcore.DEFAULT_FIRST_COLOR,
                                                   bgclr=imcore.DEFAULT_SECOND_COLOR:
                                    notebook.events.event_btnCreateRectangle(thickness=t, bgcolor=bgclr, outcolor=outclr))
        btnCreateRectangle.pack(side=TOP, pady=5)
        # frame_graphic.grid(sticky="nsew")

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
        root.config(menu=menubar)

        notebook.bind("<<NotebookTabChanged>>", notebook.select_curr_tab)



if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
