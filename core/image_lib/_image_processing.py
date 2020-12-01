""" Хранит класс-ядро для работы с изображениями

    Переменные:
        * drawQ: bool - флаг, показывающий, было ли что-то нарисовано на холсте

    Функции:
        * random_color(): -> str

    Класс:
        * Img(canvas: _custom_objects.CustomCanvas)
"""


# Импортированные модули
from tkinter import messagebox, filedialog, ALL
from PIL import Image, ImageTk, UnidentifiedImageError, EpsImagePlugin, ImageFilter, ImageEnhance
from io import BytesIO
from random import choices, randint


drawQ = False

"""
    > Нужно для сохранения изображения
    Если drawQ == True, так как в этом случае используется метод Canvas.postscript,
    который генерирует изображение в .eps формате. Для обработки этого формата PIL нужен модуль GhostScript (который
    как-то странно работает и у всех по разному, и в некоторых случаях нужно скачивать .exe файл с этим модулем, путь к
    которому как раз таки и указывается в следующей строке (хотя у Егора, например, этого не было)
"""

# EpsImagePlugin.gs_windows_binary = r'C:\Program Files\gs\gs9.53.3\bin\gswin64c'


def random_color():
    """ Герерирует случайный цвет в формате hex

        Возвращает:
            str - строку цвета в hex-формате
    """

    r = lambda: randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())


class Img:
    """
        Img - содержит все события для работы с изображениями

        Аргументы:
            * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором происходит отрисовка

        Методы:
            * set_image(self) -> None
            * get_info(self) -> None
            * save_image(self) -> None
            * return_image(self) -> None
            * set_bg(self) -> None
            * grab(self, event: tkinter.Event) -> None
            * drag(self, event: tkinter.Event) -> None
            * zoom(self, event: tkinter.Event) -> None
            * redraw(self, direction: str = "in") -> None
            * apply_filter_1(self, f: tkinter.StringVar) -> None
            * apply_filter_2(self, f: tkinter.StringVar, per: tkinter.StringVar) -> None
            * apply_filter_3(self, f: tkinter.StringVar) -> None
            * apply_filter_4(self) -> None
    """

    def __init__(self, canvas):
        self._canvas = canvas
        self._types = (("Изображение", "*.jpg *.gif *.png *.jpeg"),)
        self._y = None
        self._x = None

    def set_image(self):
        """ Устанавливает изображение на холст, если его еще нет, а если есть, то изменяет текущее

            Возвращает:
                None
        """

        try:
            page = self._canvas.img
            image = Image.open(filedialog.askopenfilename(title="Open image", filetypes=self._types))
            page["imgs"].append(image)
            photo = ImageTk.PhotoImage(image)
            im_size = image.size
            if len(self._canvas.img["imgs"]) == 1:
                page["cr_img"] = self._canvas.create_image(0, 0, anchor='nw', image=photo)
            else:
                self._canvas.itemconfig(page["cr_img"], image=photo)
            self._canvas.config(width=im_size[0], height=im_size[1])
            self._canvas.configure(scrollregion=(0, 0) + im_size)

            page["ph"] = photo
            page["img_size"] = im_size
            page["scale_size"] = im_size
            page["scale"] = 1.0

        except UnidentifiedImageError:
            messagebox.showerror("Ошибка!", "Не удалось загузить фотографию")
        except AttributeError:
            pass

    def get_info(self):
        """ Служебный метод для отладки

            Возвращает:
                None

            Побочный эффект:
                Печатает в консоль информацию о текущем холсте
        """

        print(self._canvas.img)

    def save_image(self):
        """ Сохраняет изображение с холста

            Возвращает:
                None

            Побочный эффект:
                Если drawQ, то сохраняет изображение через postscipt, если нет, то просто последнее изображение из списка изображений
        """

        new_file = filedialog.asksaveasfilename(title="Сохранить файл",
                                                defaultextension=".jpg",
                                                filetypes=self._types)
        page = self._canvas.img

        if drawQ:
            ps = self._canvas.postscript(colormode="color",
                                        height=page["scale_size"][1],
                                        width=page["scale_size"][0],
                                        x='0.c', y='0.c')
            image = Image.open(BytesIO(ps.encode('utf-8'))).resize([_ + 0 for _ in page["img_size"]])
            image = image.crop((5, 5, page["img_size"][0] - 5, page["img_size"][1] - 5))
        else:
            image = page["imgs"][-1].resize([_ + 10 for _ in page["img_size"]])
            image = image.crop((5, 5, page["img_size"][0] - 5, page["img_size"][1] - 5))
        if new_file:
            image.save(new_file)

    def return_image(self):
        """ Возвращает на холст предыдущее изображение из списка изображений, а текущее удаляет

            Возвращает:
                None
        """

        page = self._canvas.img
        if len(page["imgs"]) >= 2:
            del page["imgs"][-1]
            image = page["imgs"][-1]
            page["ph"] = ImageTk.PhotoImage(image)
            self._canvas.itemconfig(page["cr_img"], image=page["ph"])

    def set_bg(self):
        """ Меняет цвет фона на текущем холсте

            Возвращает:
                None
        """

        self._canvas["bg"] = random_color()

    def grab(self, event):
        """ Отлавливает начало перемещение холста (инструмент "рука")

            Аргументы:
                * event: tkinter.Event - событие, по которому считывается положение курсора

            Возращает:
                None

            Побочный эффект:
                Изменяет текущее значение координат курсора для правильного перемещения
        """

        self._y = event.y
        self._x = event.x

    def drag(self, event):
        """ Управление скроллами

            Аргументы:
                * event: tkinter.Event - событие, по которому считывается положение курсора

            Возращает:
                None

            Побочный эффект:
                Осуществляет движение холста (инструмент "рука"), то есть просто управляет скроллами
        """

        if self._y - event.y < 0:
            self._canvas.yview("scroll", -1, "units")
        elif self._y - event.y > 0:
            self._canvas.yview("scroll", 1, "units")
        if self._x - event.x < 0:
            self._canvas.xview("scroll", -1, "units")
        elif self._x - event.x > 0:
            self._canvas.xview("scroll", 1, "units")

        self._x = event.x
        self._y = event.y

    def zoom(self, event):
        """ Расчитывает коэффициент масштабирования при прокрутке колеса мыши

            Аргументы:
                * event: tkinter.Event - событие, по которому считывается положение курсора

            Возращает:
                None
        """

        page = self._canvas.img
        if event.delta > 0:
            page["scale"] = page["scale"] * 1.1 if page["scale"] < 8 else 8
            self.redraw("in")
        elif event.delta < 0:
            page["scale"] = page["scale"] * 0.9 if page["scale"] > 0.125 else 0.125
            self.redraw("on")

    def redraw(self, direction = "in"):
        """ Осущесвляет масшабирование в соответствии с коэффициентом масштабирования

            Аргументы:
                * direction: str - указывает направление увеличения/уменьшения масштабирования

            Возращает:
                None

            Побочный эффект:
                Перерисовывает текущее изображение и передвигает элементы на холсте с помощью метода canvas.scale
        """

        page = self._canvas.img
        if page["imgs"]:
            iw, ih = page["img_size"]
            page["scale_size"] = int(iw * page["scale"]), int(ih * page["scale"])
            image = page["imgs"][-1]
            page["ph"] = ImageTk.PhotoImage(image.resize(page["scale_size"]))
            self._canvas.itemconfig(page["cr_img"], image=page["ph"])

            self._canvas.configure(scrollregion=(0, 0) + page["scale_size"])

        self._canvas.config(width=page["scale_size"][0], height=page["scale_size"][1])
        scroll_speed = str(int(page["scroll_speed"] * pow(page["scale"], 1)))
        print(scroll_speed)
        self._canvas.configure(yscrollincrement=scroll_speed, xscrollincrement=scroll_speed)

        if direction == "in":
            self._canvas.scale(ALL, 0, 0, 1.1, 1.1)
        elif direction == "on":
            self._canvas.scale(ALL, 0, 0, 0.9, 0.9)

    def apply_filter_1(self, f):
        """ Применяет к изображению с холста фильтр из первой группы (DEFAULT_FILTERS_1)

            Аргументы:
                f: tkinter.StringVar - строковая переменная tkinter, в которой содержится выбранный фильтр

            Возвращает:
                None
        """

        page = self._canvas.img
        if page["imgs"]:
            image = page["imgs"][-1]
            fltr = f.get()
            image_new = None
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
            page["imgs"].append(image_new)
            page["ph"] = ImageTk.PhotoImage(image_new.resize(page["scale_size"]))
            self._canvas.itemconfig(page["cr_img"], image=page["ph"])
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")

    def apply_filter_2(self, f, per):
        """ Применяет к изображению с холста фильтр из второй группы (DEFAULT_FILTERS_2)

            Аргументы:
                f: tkinter.StringVar - строковая переменная tkinter, в которой содержится выбранный фильтр
                per: tkinter.StringVat - строковая переменная tkinter, в которой содержится процент применения фильтра

            Возвращает:
                None
        """

        page = self._canvas.img
        if page["imgs"]:
            if per.get().lstrip("-").isnumeric():
                percent = float(per.get()) / 100
                fltr = f.get()
                image = page["imgs"][-1]
                image_new = None
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
                page["ph"] = ImageTk.PhotoImage(image_new.resize(page["scale_size"]))
                self._canvas.itemconfig(page["cr_img"], image=page["ph"])
            else:
                messagebox.showerror("Внимание!", "Значение должно быть числовым")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")

    def apply_filter_3(self, f):
        """ Применяет к изображению с холста фильтр из третьей группы (DEFAULT_FILTERS_3)

            Аргументы:
                f: tkinter.StringVar - строковая переменная tkinter, в которой содержится выбранный фильтр

            Возвращает:
                None
        """

        page = self._canvas.img
        if page["imgs"]:
            fltr = f.get()
            w, h = page["img_size"][0], page["img_size"][1]
            image = page["imgs"][-1]
            mode = None
            if image.mode != "RGB":
                mode = image.mode
                image = image.convert("RGB")
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
            if mode:
                image = image.convert(mode)
            page["imgs"].append(image_new)
            page["ph"] = ImageTk.PhotoImage(image_new.resize(page["scale_size"]))
            self._canvas.itemconfig(page["cr_img"], image=page["ph"])
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")

    def apply_filter_4(self):
        """ Применяет к изображению с холста треш-фильтр

            Возвращает:
                None
        """

        page = self._canvas.img
        if page["imgs"]:
            try:
                colors = page["imgs"][-1].split()
                sample = choices(colors, k=len(colors))
                image_new = Image.merge(page["imgs"][-1].mode, sample)
                page["imgs"].append(image_new)
                page["ph"] = ImageTk.PhotoImage(image_new.resize(page["scale_size"]))
                self._canvas.itemconfig(page["cr_img"], image=page["ph"])
            except ValueError:
                messagebox.showerror("Ошибка!", "Применить фильтр не удалось")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")
