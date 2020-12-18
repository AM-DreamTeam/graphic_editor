# Импортированные модули
from tkinter import StringVar, Toplevel, messagebox
import tkinter.ttk as ttk
from PIL import Image, ImageTk


class CompressWindow(Toplevel):
    """ CompressWindow - модальное окно для настройки уровня компрессии изображения

        Аргументы:
            * root: tkinter.Tk - главное окно

        Методы:
            * submit(self) -> None
            * open(self) -> None
    """

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        ico = Image.open('images/visualist.png')
        ico.thumbnail((64, 64), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)

        self.frame_ddd = ttk.Frame(self)
        self._compress = StringVar(self.frame_ddd)
        self._compress.set("75")
        __label = ttk.Label(self.frame_ddd, text="Укажите степень сжатия изображения (Рекомендуется 75%)", font=("courier", 10))
        __entry_compress = ttk.Entry(self.frame_ddd, textvariable=self._compress)
        __button = ttk.Button(self.frame_ddd, text="Применить", command=self.submit)

        self.frame_ddd.pack()
        __label.pack(padx=20, pady=20)
        __entry_compress.pack(pady=5, ipadx=2, ipady=2)
        __button.pack(pady=5, ipadx=2, ipady=2)

        self.resizable(False, False)

    def submit(self):
        """ Событие для кнопки __button

            Возвращает:
                None

            Побочный эффект:
                Закрывает текущее модальное окно, если всё подходит под условие выхода
        """

        if self._compress.get().isdigit():
            __c = int(self._compress.get())
            if 0 <= __c <= 100:
                self.destroy()
            else:
                messagebox.showerror(title="Ошибка!", message="Значение должно быть в диапазоне от 0 до 100!")
        else:
            messagebox.showerror(title="Ошибка!", message="Значение должно быть числовым")

    def open(self):
        """ Возвращает данные на главное окно

            Возвращает:
                int: процент компрессии
        """
        self.grab_set()
        self.wait_window()
        compress = int(self._compress.get())
        return compress

