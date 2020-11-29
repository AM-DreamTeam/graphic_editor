from tkinter import *
from compressionRecognition import core


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')

        self.entry = Entry(self)
        self.entry.grid(row=2, column=0)

        self.textRecognition = Label(self)
        self.textRecognition.grid(row=0, column=1)

        tr = core.Features(self.textRecognition, self.entry)

        self.recognition = Button(self, text="распознание текста", command=tr.recognitionText)
        self.compression = Button(self, text="сжатие изображения", command=tr.imageСompression)

        self.recognition.grid(row=0, column=0, sticky=NW)
        self.compression.grid(row=1, column=0, sticky=NW)


if __name__ == "__main__":
    app = App()
    app.mainloop()
