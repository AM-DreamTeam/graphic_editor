from tkinter import *
from image_lib import _image_core as core


class App:
    def __init__(self, root):
        root.geometry('800x600')
        # root.state('zoomed')

        # фрейм для кпопок
        frame_btn = Frame(root)

        # инициализуем Notebook
        notebook = core.CustomNotebook(root)
        notebook.grid(row=0, column=1, sticky="nswe")

        # кнопка возврата предыдущего изображения
        Button(frame_btn,
               text="return image",
               command=notebook.image_processing.return_image
               ).pack(pady=10)

        # кнопка создания новой вкладки
        Button(frame_btn,
               text="new canvas",
               command=notebook.create_new_canvas
               ).pack(pady=10)

        # кнопка смены увета фона
        Button(frame_btn,
               text="bg",
               command=lambda: notebook.image_processing.set_bg()
               ).pack(pady=10)

        # выводит на экран информацию о текущем холсте - для отладки
        Button(frame_btn,
               text="get info",
               command=lambda: notebook.image_processing.get_info()
               ).pack(pady=10)

        # кнопки фильтра 1

        # создаем выпадающее меню
        frame_filter1 = Frame(frame_btn)
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
        frame_filter1.pack(pady=10)

        # кнопки фильтра 2

        # все тоже самое, только еще есть поле Entry, в которое вводится значение коэффициента,
        # при котором происходит фильтрация
        frame_filter2 = Frame(frame_btn)
        variable_filter_2 = StringVar(frame_filter2)
        variable_filter_2.set(core.DEFAULT_FILTERS_2[0])
        filters2 = OptionMenu(frame_filter2,
                              variable_filter_2,
                              *core.DEFAULT_FILTERS_2
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
        frame_filter3 = Frame(frame_btn)
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
        frame_filter3.pack(pady=10)

        # фильтр 4
        Button(frame_btn,
               text="try your luck",
               command=lambda: notebook.image_processing.apply_filter_4()
               ).pack(pady=10)

        frame_btn.grid(row=0, column=0, rowspan=2, sticky="nsew")

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
