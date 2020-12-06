from tkinter import StringVar, Toplevel, Entry, Label, Button, messagebox

class CompressWindow(Toplevel):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self._compress = StringVar(self)
        self._compress.set("75")
        __label = Label(self, text="Укажите степень сжатия изображения (Рекомендуется 75%)")
        __entry_compress = Entry(self, textvariable=self._compress)
        __button = Button(self, text="Применить", command=self.submit)

        __label.pack(padx=20, pady=20)
        __entry_compress.pack(pady=5, ipadx=2, ipady=2)
        __button.pack(pady=5, ipadx=2, ipady=2)


    def submit(self):
        if self._compress.get().isdigit():
            __c = int(self._compress.get())
            if 0 <= __c <= 100:
                self.destroy()
            else:
                messagebox.showerror(title="Ошибка!", message="Значение должно быть в диапазоне от 0 до 100!")
        else:
            messagebox.showerror(title="Ошибка!", message="Значение должно быть числовым")

    def open(self):
        self.grab_set()
        self.wait_window()
        compress = int(self._compress.get())
        return compress

