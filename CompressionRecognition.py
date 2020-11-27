from pathlib import Path
from tkinter import *
from tkinter import filedialog

import cv2
import pytesseract
from PIL import Image


def imageСompression(quality=30):

    """ сжатие изображения """

    files = filedialog.askopenfilenames()
    for image in files:
        Image.open(image).save('condensed' + image[image.rindex('/') + 1:], optimize=True, quality=quality)


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')

        recognition = Button(self, text="распознание текста", command=self.recognitionText)
        compression = Button(self, text="сжатие изобра", command=imageСompression)

        recognition.grid(row=0, column=0, sticky=NW)
        compression.grid(row=1, column=0, sticky=NW)

    def recognitionText(self):

        """ распознаёт текст на изображении """

        files = filedialog.askopenfilenames()
        nameFile = Path(files[0]).name
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        img = cv2.imread(nameFile)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        text = Label(self, text=pytesseract.image_to_string(img, lang='rus'))
        text.grid(row=0, column=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
