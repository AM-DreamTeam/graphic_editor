from pathlib import Path
from tkinter import *
from tkinter import filedialog
from os import path

import os
import cv2
import pytesseract
from PIL import Image


class Features:
    def __init__(self, label, entry):
        self.label = label
        self.entry = entry

    def recognitionText(self):

        """ распознаёт текст на изображении """

        files = filedialog.askopenfilenames()[0]
        old_file = os.path.join(files[:files.rindex('/')], Path(files).name)
        new_file = os.path.join(files[:files.rindex('/')], 'rer' + path.splitext(Path(files).name)[1])
        os.rename(old_file, new_file)

        new_file = new_file.replace('/', '\\')

        nameFile = Path(new_file).name
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        img = cv2.imread(nameFile)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.label['text'] = pytesseract.image_to_string(img, lang='rus')

        old_file = os.path.join(files[:files.rindex('/')], 'rer' + path.splitext(Path(files).name)[1])
        new_file = os.path.join(files[:files.rindex('/')], Path(files).name)
        os.rename(old_file, new_file)

    def imageСompression(self):

        """ сжатие изображения """

        quality = self.entry.get()
        if quality.isdigit():
            quality = int(quality)
        else:
            quality = 30

        files = filedialog.askopenfilenames()
        for image in files:
            Image.open(image).save('condensed ' + Path(image).name, optimize=True, quality=quality)
