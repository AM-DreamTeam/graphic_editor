from tkinter import *
import functions


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')

        entry = Entry(self)
        entry.grid(row=2, column=0)

        textRecognition = Label(self)
        textRecognition.grid(row=0, column=1)

        tr = functions.Features(textRecognition, entry)

        recognition = Button(self, text="распознание текста", command=tr.recognitionText)
        compression = Button(self, text="сжатие изображения", command=tr.imageСompression)

        recognition.grid(row=0, column=0, sticky=NW)
        compression.grid(row=1, column=0, sticky=NW)


if __name__ == "__main__":
    app = App()
    app.mainloop()
