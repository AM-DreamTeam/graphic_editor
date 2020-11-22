from tkinter import *
from io import BytesIO
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
from PIL import EpsImagePlugin


#нужно для того, чтобы нормально работало получение изображения с Canvas
EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs9.53.3\bin\gswin64c'

#кастомный canvas
class CustomCanvas(Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.root = master


    def set_image(self):
        '''
        загружает фотографию, которую выбирает пользователь в всплывающем меню
        и прикрепляет ее к master, при этом canvas обрезается по размерам загруженного изображения
        '''
        try:
            self.image = Image.open(filedialog.askopenfilename())
            self.photo = ImageTk.PhotoImage(self.image)
            self.im_size = self.image.size
            #print(f'photo{self.im_size}')
            self.image = self.create_image(0, 0, anchor='nw',image=self.photo)
            self.config(width=self.im_size[0], height=self.im_size[1])

            self.grid()
        except UnidentifiedImageError:
            messagebox.showinfo('Ошибка!', 'Не удалось загузить фотографию')
        except AttributeError:
            pass

    def get_image(self):
        """
        получает текущее изображение с canvas и конвертирует его в формат, поддерживаемый Pillow
        нужно оптимизировать, так как работает долго
        """
        ps = self.postscript(colormode='color', height=self["height"], width=self["width"], x = '0.0', y = '0.0')
        return Image.open(BytesIO(ps.encode('utf-8')))

    def save_image(self):
        """
        сохраняет текущее изображение с canvas (пока тест-версия, но уже рабочая)
        """
        self.get_image().save(r"graphic_editor\tkinter + pil\test.jpg")


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        #self.state('zoomed')


        """
        два фрейма, один для кнопок, другой для canvas'a
        """
        self.frame_bn = Frame(self).grid()
        self.frame_cv = Frame(self).grid()


        """
        scrollbar'ы для canvas
        """
        self.scroll_x = Scrollbar(self.frame_cv, orient=HORIZONTAL)
        self.scroll_y = Scrollbar(self.frame_cv, orient=VERTICAL)

        self.canvas = CustomCanvas(self.frame_cv, width=800, height=600,
                                xscrollcommand=self.scroll_x.set,
                                yscrollcommand=self.scroll_y.set,
                                bg='#E0FFFF')
        self.scroll_x.config(command=self.canvas.xview)
        self.scroll_y.config(command=self.canvas.yview)

        """
        кнопки - как пример того, что будет при обработке фото
        пока что назначил команды для удобства отладки
        """
        self.but1 = Button(self.frame_bn, text="get image", command=self.canvas.get_image).grid()
        self.but2 = Button(self.frame_bn, text="get size", command=lambda: print(self.canvas["width"], self.canvas['height'])).grid()

        """
        frame для canvas'a, чтобы scrollbar корректно работал

        подробнее тут - https://pythonru.com/uroki/sozdanie-skrollbarov-tkinter-6
        """
        self.cv_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.cv_frame,
                                  anchor=N + W)

        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.scroll_x.grid(row=1, column=0, sticky="we")
        self.scroll_y.grid(row=0, column=1, sticky="ns")


        """
        для корректного отображения canvas'a
        """
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.bind("<Configure>", self.resize)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())


        """
        меню с доступными командами
        """
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.canvas.set_image)
        filemenu.add_command(label="Save", command=self.canvas.save_image)
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
