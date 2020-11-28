from tkinter import *
from tkinter.ttk import Notebook
from image_lib import core



class App():
    def __init__(self, root):
        root.geometry('800x600')
        #root.state('zoomed')


        #фрейм для кпопок
        frame_btn = Frame(root)

        notebook = Notebook(root)
        #scrollbar'ы для canvas
        scroll_x = Scrollbar(root, orient=HORIZONTAL)
        scroll_y = Scrollbar(root, orient=VERTICAL)


        canvas = Canvas(notebook, width=800, height=600,
                                xscrollcommand=scroll_x.set,
                                yscrollcommand=scroll_y.set,
                                bg='#E0FFFF')

        notebook.add(canvas, text="Холст 1")
        self.selected_tab = canvas


        scroll_x.config(command=canvas.xview)
        scroll_y.config(command=canvas.yview)

        notebook.grid(row=0, column=1, sticky="nswe")
        scroll_x.grid(row=1, column=1, sticky="we")
        scroll_y.grid(row=0, column=2, sticky="ns")

        #подключение модуля обработки фото
        image_processing = core.Img(notebook, canvas, scroll_x, scroll_y)

        #кнопка возврата предыдущего изображения
        Button(frame_btn, text="return image",
                command=image_processing.return_image).pack(pady=10)

        Button(frame_btn, text="new canvas",
                command=image_processing.create_new_canvas).pack(pady=10)

        Button(frame_btn, text="bg",
                command=image_processing.set_bg).pack(pady=10)


        #кнопки фильтра 1
        frame_filter1 = Frame(frame_btn)
        variable_filter_1 = StringVar(frame_filter1)
        variable_filter_1.set(core.DEFAULT_FILTERS_1[0])
        filters1 = OptionMenu(frame_filter1, variable_filter_1,
                                *core.DEFAULT_FILTERS_1)
        filters1.grid(row=0, sticky="we")


        btnApplyFilter1 = Button(frame_filter1,
                                text="apply filter",
                                command=lambda x=variable_filter_1:
                                image_processing.apply_filter_1(x))
        btnApplyFilter1.grid(row=1, sticky="e")
        frame_filter1.pack(pady=10)


        #кнопки фильтра 2
        frame_filter2 = Frame(frame_btn)
        variable_filter_2 = StringVar(frame_filter2)
        variable_filter_2.set(core.DEFAULT_FILTERS_2[0])
        filters2 = OptionMenu(frame_filter2, variable_filter_2,
                                *core.DEFAULT_FILTERS_2)
        filters2.grid(row=0, sticky="we", columnspan=2)

        variable_filter_2_percent = StringVar(frame_filter2)
        variable_filter_2_percent.set(100)
        entry_filter2 = Entry(frame_filter2,
                                textvariable=variable_filter_2_percent)
        entry_filter2.grid(row=1, column=0)
        Label(frame_filter2, text="%").grid(row=1, column=1)

        btnApplyFilter2 = Button(frame_filter2,
                                text="apply filter",
                                command=lambda
                                x=variable_filter_2,
                                y=variable_filter_2_percent:
                                image_processing.apply_filter_2(x, y))
        btnApplyFilter2.grid(row=2, column=0, columnspan=2, sticky="we")
        frame_filter2.pack(pady=10)


        #кнопки фильтра 3
        frame_filter3 = Frame(frame_btn)
        variable_filter_3 = StringVar(frame_filter1)
        variable_filter_3.set(core.DEFAULT_FILTERS_3[0])
        filters3 = OptionMenu(frame_filter3, variable_filter_3,
                            *core.DEFAULT_FILTERS_3)
        filters3.grid(row=0, column=0, columnspan=2, sticky="we")


        btnApplyFilter3 = Button(frame_filter3,
                                text="apply filter",
                                command=lambda x=variable_filter_3:
                                image_processing.apply_filter_3(x))
        btnApplyFilter3.grid(row=1, column=0, columnspan=2, sticky="e")
        frame_filter3.pack(pady=10)



        #фильтр 4
        Button(frame_btn, text="try your luck",
                command=image_processing.apply_filter_4).pack(pady=10)

        frame_btn.grid(row=0, column=0, rowspan=2, sticky="nsew")


        #для корректного отображения canvas'а
        root.rowconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.bind("<Configure>", image_processing.resize)
        root.update_idletasks()
        root.minsize(root.winfo_width(), root.winfo_height())




        #меню с доступными командами
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=image_processing.set_image)
        filemenu.add_command(label="Save", command=image_processing.save_image)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)


        self.selected_tab.bind("<Button 3>", image_processing.grab)
        self.selected_tab.bind("<B3-Motion>", image_processing.drag)


        notebook.bind("<<NotebookTabChanged>>", image_processing.select_curr_tab)

        # root.bind("<MouseWheel>", image_processing.zoom)



    def bind_tab(self, event):
        self.selected_tab = event.widget.select()
        print(self.selected_tab)


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
