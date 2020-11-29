from tkinter import *
from compressionRecognition import core


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600') # размеры окна

        self.entry = Entry(self) # поле ввода для качества сжимения изображения
        self.entry.grid(row=2, column=0)

        self.textRecognition = Label(self) # место ввывода для распознования текста
        self.textRecognition.grid(row=0, column=1)

        tr = core.Features(self.textRecognition, self.entry) # объект каласса, где есть необходимые функции

        self.recognition = Button(self, text="распознание текста", command=tr.recognitionText) # для распознования
        self.compression = Button(self, text="сжатие изображения", command=tr.imageСompression) # для сжатия

        self.recognition.grid(row=0, column=0, sticky=NW)
        self.compression.grid(row=1, column=0, sticky=NW)


if __name__ == "__main__":
    app = App()
    app.mainloop()
