from pathlib import Path
from tkinter import *
from tkinter import filedialog

import cv2
import pytesseract
from PIL import Image


class Features:
    def __init__(self, label, entry):
        self.label = label
        self.entry = entry

    def recognitionText(self):

        """ распознаёт текст на изображении """

        files = filedialog.askopenfilenames()
        nameFile = Path(files[0]).name
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        img = cv2.imread(nameFile)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.label['text'] = pytesseract.image_to_string(img, lang='rus')

    def imageСompression(self, quality=30):

        """ сжатие изображения """

        if self.entry.get() != '':
            quality = int(self.entry.get())

        files = filedialog.askopenfilenames()
        for image in files:
            Image.open(image).save('condensed' + image[image.rindex('/') + 1:], optimize=True, quality=quality)
