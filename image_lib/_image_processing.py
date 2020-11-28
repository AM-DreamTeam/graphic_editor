from tkinter import Canvas, messagebox, filedialog, ALL
from PIL import Image, ImageTk, UnidentifiedImageError, EpsImagePlugin, ImageFilter, ImageEnhance
from io import BytesIO
from random import choices, randint
from pprint import pprint
# from ._custom_objects import *



EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs9.53.3\bin\gswin64c'

def random_color():
    r = lambda: randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())



class Img:
    def __init__(self, notebook, canvas, scroll_x, scroll_y):
        self.notebook = notebook
        canvas.configure(yscrollincrement='11', xscrollincrement='11')

        self.canvases = {1: {"cnv": canvas, "imgs": [], "cr_img": None, "img_size": (800, 600), "ph": None}}
        self.canvas_id = 1

        self.types = (("Изображение", "*.jpg *.gif *.png *.jpeg"),)

        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.scale = 1.0

    def create_new_canvas(self):
        """
        Создает новую вкладку на notebook и размещает на нем новый холст
        """

        canvas = Canvas(self.notebook, width=800, height=600, bg=random_color(),xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        canvas.configure(yscrollincrement='11', xscrollincrement='11')
        self.scroll_x.config(command=canvas.xview)
        self.scroll_y.config(command=canvas.yview)

        self.canvas_id = len(self.canvases) + 1
        self.notebook.add(canvas, text=f"Холст {self.canvas_id}")
        self.notebook.select(self.canvas_id - 1)
        self.canvases[self.canvas_id] = {"cnv": canvas, "imgs": [], "cr_img": None, "img_size": (800, 600), "ph": None}
        # pprint(self.canvases)


    def select_curr_tab(self, event):
        """
        Изменяет self.canvas_id на номер текущей открытой вкладки
        """
        selected_tab = event.widget.select()
        tab_name = event.widget.tab(selected_tab, "text")
        self.canvas_id = int(tab_name[-1])
        self.resize("<Configure>")


    def grab(self, event):
        """
        Отлавливает начало перемещания холста (инструмент "рука", и изменяет
        текущее значение координат курсора для правильного перемещения
        """
        # print("grab")
        self._y = event.y
        self._x = event.x


    def drag(self,event):
        """
        Осуществляет движение холста (инструмент "рука")
        """
        # print("drag")
        canvas = self.canvases[self.canvas_id]["cnv"]
        if (self._y-event.y < 0):
            canvas.yview("scroll",-1,"units")
        elif (self._y-event.y > 0):
            canvas.yview("scroll",1,"units")
        if (self._x-event.x < 0):
            canvas.xview("scroll",-1,"units")
        elif (self._x-event.x > 0):
            canvas.xview("scroll",1,"units")
        self._x = event.x
        self._y = event.y


    def resize(self, event):
        """
        Метод resize обрабатывает событие изменения размера окна и обновляет
        параметр scrollregion, определяющий область Canvas, которую можно
        скроллить.
        """

        try:
            page = self.canvases[self.canvas_id]
            page["cnv"].configure(scrollregion=(0, 0) + page["img_size"])
            self.scroll_x.config(command=page["cnv"].xview)
            self.scroll_y.config(command=page["cnv"].yview)
        except KeyError:
            pass


    def set_bg(self):
        page = self.canvases[self.canvas_id]
        canvas = page["cnv"]
        canvas["bg"]=random_color()


    def set_image(self):

        """
        Устанавливает изображение на холст
        """
        try:
            page = self.canvases[self.canvas_id]
            canvas = page["cnv"]

            image = Image.open(filedialog.askopenfilename(title="Open image",
                                                                filetypes=self.types))

            page["imgs"].append(image)
            page["ph"] = ImageTk.PhotoImage(image)
            im_size = image.size
            page["img_size"] = im_size


            page["cr_img"] = page["cnv"].create_image(0, 0, anchor='nw',
                                                        image=page["ph"])
            # pprint(self.canvases)
            canvas.config(width=im_size[0], height=im_size[1])
            canvas.configure(scrollregion=(0, 0) + im_size)


        except UnidentifiedImageError:
            messagebox.showerror('Ошибка!', 'Не удалось загузить фотографию')
        except AttributeError:
            pass


    def save_image(self):
        """
        Сохраняет изображение с холста
        """
        new_file = filedialog.asksaveasfilename(title="Сохранить файл",
                                                defaultextension=".jpg",
                                                filetypes=self.types)
        page = self.canvases[self.canvas_id]
        ps = page["cnv"].postscript(colormode="color",
                                    height=page["cnv"]["height"],
                                    width=page["cnv"]["width"],
                                    x = '0.c', y = '0.c')
        image = Image.open(BytesIO(ps.encode('utf-8'))).resize([_ + 0 for _ in page["img_size"]])
        image = image.crop((5, 5, page["img_size"][0] - 5, page["img_size"][1] - 5))
        if new_file:
            image.save(new_file)


    def return_image(self):
        """
        Возвращает на холст предыдущее изображение
        """
        page = self.canvases[self.canvas_id]
        if len(page["imgs"]) >= 2:
            del page["imgs"][-1]
            image = page["imgs"][-1]
            page["ph"] = ImageTk.PhotoImage(image)
            page["cnv"].itemconfig(page["cr_img"], image=page["ph"])


    def apply_filter_1(self, f):
        """
        Прирменяет к изображению с холста фильтр из первой группы
        (DEFAULT_FILTERS_1)
        """
        page = self.canvases[self.canvas_id]
        if page["imgs"]:
            image = page["imgs"][-1]
            fltr = f.get()
            if fltr == "blur":
                image_new = image.filter(ImageFilter.BLUR)
            elif fltr == "contour":
                image_new = image.filter(ImageFilter.CONTOUR)
            elif fltr == "detail":
                image_new = image.filter(ImageFilter.DETAIL)
            elif fltr == "edge enhance":
                image_new = image.filter(ImageFilter.EDGE_ENHANCE)
            elif fltr == "emboss":
                image_new = image.filter(ImageFilter.EMBOSS)
            elif fltr == "find edges":
                image_new = image.filter(ImageFilter.FIND_EDGES)
            elif fltr == "sharpen":
                image_new = image.filter(ImageFilter.SHARPEN)
            elif fltr == "smooth":
                image_new = image.filter(ImageFilter.SMOOTH)
            else:
                pass
            page["imgs"].append(image_new)
            page["ph"] = ImageTk.PhotoImage(image_new)
            page["cnv"].itemconfig(page["cr_img"], image=page["ph"])
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")


    def apply_filter_2(self, f, per):
        """
        Прирменяет к изображению с холста фильтр из второй группы
        (DEFAULT_FILTERS_2)
        """
        page = self.canvases[self.canvas_id]
        if page["imgs"]:
            if per.get().lstrip("-").isnumeric():
                percent = float(per.get())/100
                fltr = f.get()
                image = page["imgs"][-1]
                if fltr == "color":
                    image_new = ImageEnhance.Color(image).enhance(percent)
                elif fltr == "contrast":
                    image_new = ImageEnhance.Contrast(image).enhance(percent)
                elif fltr == "brightness":
                    image_new = ImageEnhance.Brightness(image).enhance(percent)
                elif fltr == "sharpness":
                    image_new = ImageEnhance.Sharpness(image).enhance(percent)
                else:
                    pass
                page["imgs"].append(image_new)
                page["ph"] = ImageTk.PhotoImage(image_new)
                page["cnv"].itemconfig(page["cr_img"], image=page["ph"])
            else:
                messagebox.showerror("Внимание!", "Значение должно быть числовым")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")


    def apply_filter_3(self, f):
        """
        Прирменяет к изображению с холста фильтр из третьей группы
        (DEFAULT_FILTERS_3)
        """
        page = self.canvases[self.canvas_id]
        if page["imgs"]:
            fltr = f.get()
            w, h = page["img_size"][0], page["img_size"][1]
            image = page["imgs"][-1]
            image_new = Image.new('RGB', (w, h))

            if fltr == "negative":
                for x in range(w):
                    for y in range(h):
                        r, g, b = image.getpixel((x, y))
                        image_new.putpixel((x, y), (255 - r, 255 - g, 255 - b))
            elif fltr == "white-black":
                separator = 255 / 0.8 / 2 * 3
                for x in range(w):
                    for y in range(h):
                        r, g, b = image.getpixel((x, y))
                        total = r + g + b
                        if total > separator:
                            image_new.putpixel((x, y), (255, 255, 255))
                        else:
                            image_new.putpixel((x, y), (0, 0, 0))
            elif fltr == "gray scale":
                for x in range(w):
                    for y in range(h):
                        r, g, b = image.getpixel((x, y))
                        gray = int(r * 0.2126 + g * 0.7152 + b * 0.0722)
                        image_new.putpixel((x, y), (gray, gray, gray))
            elif fltr == "sepia":
                for x in range(w):
                    for y in range(h):
                        r, g, b = image.getpixel((x, y))
                        red = int(r * 0.393 + g * 0.769 + b * 0.189)
                        green = int(r * 0.349 + g * 0.686 + b * 0.168)
                        blue = int(r * 0.272 + g * 0.534 + b * 0.131)
                        image_new.putpixel((x, y), (red, green, blue))
            else:
                pass
            page["imgs"].append(image_new)
            page["ph"] = ImageTk.PhotoImage(image_new)
            page["cnv"].itemconfig(page["cr_img"], image=page["ph"])
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")


    def apply_filter_4(self):
        page = self.canvases[self.canvas_id]
        if page["imgs"]:
            try:
                colors = page["imgs"][-1].split()
                sample = choices(colors, k=len(colors))
                image_new = Image.merge(page["imgs"][-1].mode, sample)
                page["imgs"].append(image_new)
                page["ph"] = ImageTk.PhotoImage(image_new)
                page["cnv"].itemconfig(page["cr_img"], image=page["ph"])
            except ValueError:
                messagebox.showerror("Ошибка!", "Применить фильтр не удалось")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")
