from tkinter import Canvas, messagebox, filedialog, ALL
from PIL import Image, ImageTk, UnidentifiedImageError, EpsImagePlugin, ImageFilter, ImageEnhance
from io import BytesIO
from random import choices

EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs9.53.3\bin\gswin64c'

class Img:
    def __init__(self, canvas):
        self.canvas = canvas
        self.types = (("Изображение", "*.jpg *.gif *.png *.jpeg"),)
        self.image = None
        self.images = []

    def set_image(self):
        """
        Устанавливает изображение на холст
        """
        try:
            self.image = Image.open(filedialog.askopenfilename(title="Open image", filetypes=self.types))
            self.images.append(self.image)
            self.photo = ImageTk.PhotoImage(self.image)
            self.im_size = self.image.size
            self.canvas.create_image(0, 0, anchor='nw',image=self.photo)
            self.canvas.config(width=self.im_size[0], height=self.im_size[1])
            self.canvas.configure(scrollregion=(0, 0) + self.im_size)

            self.canvas.grid()
        except UnidentifiedImageError:
            messagebox.showerror('Ошибка!', 'Не удалось загузить фотографию')
        except AttributeError:
            pass

    def get_image(self):
        """
        Снимает изображение с холста
        """
        ps = self.canvas.postscript(colormode="color",  height=self.canvas["height"], width=self.canvas["width"], x = '0.c', y = '0.c')
        self.image = Image.open(BytesIO(ps.encode('utf-8'))).resize(self.im_size)
        self.images.append(self.image)
        return self.image


    def save_image(self):
        """
        Сохраняет изображение с холста
        """
        new_file = filedialog.asksaveasfilename(title="Сохранить файл", defaultextension=".jpg", filetypes=self.types)
        self.image = self.get_image()
        print(self.image.size)
        if new_file:
            self.image.save(new_file)

    def return_image(self):
        """
        Возвращает на холст предыдущее изображение
        """
        if len(self.images) >= 2:
            del self.images[-1]
            self.image = self.images[-1]
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor='nw',image=self.photo)


    def apply_filter_1(self, f):
        """
        Прирменяет к изображению с холста фильтр из первой группы (DEFAULT_FILTERS_1)
        """
        if self.image:
            self.image = self.get_image()
            fltr = f.get()
            if fltr == "blur":
                self.photo = ImageTk.PhotoImage(self.image.filter(ImageFilter.BLUR))
            elif fltr == "contour":
                self.photo = ImageTk.PhotoImage(self.image.filter(ImageFilter.CONTOUR))
            elif fltr == "detail":
                self.photo = ImageTk.PhotoImage(self.image.filter(ImageFilter.DETAIL))
            elif fltr == "edge enhance":
                self.photo = ImageTk.PhotoImage(self.image.filter(ImageFilter.EDGE_ENHANCE))
            elif fltr == "emboss":
                self.photo = ImageTk.PhotoImage(self.image.filter(ImageFilter.EMBOSS))
            elif fltr == "find edges":
                self.photo = ImageTk.PhotoImage(self.image.filter(ImageFilter.FIND_EDGES))
            elif fltr == "sharpen":
                self.photo = ImageTk.PhotoImage(self.image.filter(ImageFilter.SHARPEN))
            elif fltr == "smooth":
                self.photo = ImageTk.PhotoImage(self.image.filter(ImageFilter.SMOOTH))
            else:
                pass

            self.canvas.create_image(0, 0, anchor='nw',image=self.photo)
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")


    def apply_filter_2(self, f, per):
        """
        Прирменяет к изображению с холста фильтр из второй группы (DEFAULT_FILTERS_2)
        """
        if self.image:
            if per.get().lstrip("-").isnumeric():
                percent = float(per.get())/100
                self.image = self.get_image()
                fltr = f.get()
                if fltr == "color":
                    self.photo = ImageTk.PhotoImage(ImageEnhance.Color(self.image).enhance(percent))
                elif fltr == "contrast":
                    self.photo = ImageTk.PhotoImage(ImageEnhance.Contrast(self.image).enhance(percent))
                elif fltr == "brightness":
                    self.photo = ImageTk.PhotoImage(ImageEnhance.Brightness(self.image).enhance(percent))
                elif fltr == "sharpness":
                    self.photo = ImageTk.PhotoImage(ImageEnhance.Sharpness(self.image).enhance(percent))
                else:
                    pass
                self.canvas.create_image(0, 0, anchor='nw',image=self.photo)
            else:
                messagebox.showerror("Внимание!", "Значение должно быть числовым")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")


    def apply_filter_3(self, f):
        """
        Прирменяет к изображению с холста фильтр из третьей группы (DEFAULT_FILTERS_3)
        """
        if self.image:
            fltr = f.get()
            self.image = self.get_image()
            w, h = self.im_size[0], self.im_size[1]
            new = Image.new('RGB', (w, h))
            if fltr == "negative":
                for x in range(w):
                    for y in range(h):
                        r, g, b = self.image.getpixel((x, y))
                        new.putpixel((x, y), (255 - r, 255 - g, 255 - b))
            elif fltr == "white-black":
                separator = 255 / 0.8 / 2 * 3
                for x in range(w):
                    for y in range(h):
                        r, g, b = self.image.getpixel((x, y))
                        total = r + g + b
                        if total > separator:
                            new.putpixel((x, y), (255, 255, 255))
                        else:
                            new.putpixel((x, y), (0, 0, 0))
            elif fltr == "gray scale":
                for x in range(w):
                    for y in range(h):
                        r, g, b = self.image.getpixel((x, y))
                        gray = int(r * 0.2126 + g * 0.7152 + b * 0.0722)
                        new.putpixel((x, y), (gray, gray, gray))
            elif fltr == "sepia":
                for x in range(w):
                    for y in range(h):
                        r, g, b = self.image.getpixel((x, y))
                        red = int(r * 0.393 + g * 0.769 + b * 0.189)
                        green = int(r * 0.349 + g * 0.686 + b * 0.168)
                        blue = int(r * 0.272 + g * 0.534 + b * 0.131)
                        new.putpixel((x, y), (red, green, blue))
            else:
                pass

            self.photo = ImageTk.PhotoImage(new)
            self.canvas.create_image(0, 0, anchor='nw',image=self.photo)
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")


    def apply_filter_4(self):
        if self.image:
            self.image = self.get_image()
            colors = self.image.split()
            sample = choices(colors, k=len(colors))
            self.photo = ImageTk.PhotoImage(Image.merge(self.image.mode, sample))
            self.canvas.create_image(0, 0, anchor='nw',image=self.photo)
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")
