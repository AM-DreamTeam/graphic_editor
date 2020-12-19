# Импортированные модули
from tkinter import messagebox, filedialog, ALL
from PIL import Image, ImageTk, UnidentifiedImageError, EpsImagePlugin, ImageFilter, ImageEnhance, ImageOps
from io import BytesIO
from random import choices
from copy import copy
from core.image_lib._compress_window import CompressWindow
from core.graphic_lib._basic import select_style


class Img:
    """
        Img - содержит все события для работы с изображениями

        Аргументы:
            * root: tkinter.Tk - главное окно
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
            * zoom_in(self, event: tkinter.Event) -> None
            * zoom_off(self, event: tkinter.Event) -> None
            * update_data(self, const: float) -> None
            * redraw(self, direction: str = "in") -> None
            * apply_filter_1(self, f: tkinter.StringVar) -> None
            * apply_filter_2(self, f: tkinter.StringVar, per: tkinter.StringVar) -> None
            * apply_filter_3(self, f: tkinter.StringVar) -> None
            * apply_filter_4(self) -> None
            * change_layers(self, red: tkinter.Scale, green: tkinter.Scale, blue: tkinter.Scale, event: tkinter.Event) -> None
            * normalize_image(self) -> None
            * append_image(self) -> None
            * reflect_image(self, direction: str) -> None
            * rotate_image(self, direction: str) -> None
    """

    def __init__(self, root, canvas):
        self.root = root
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
            self._canvas.saveQ = False
            __page = self._canvas.img
            __image = Image.open(filedialog.askopenfilename(title="Open image", filetypes=self._types))
            __page["imgs"].append(__image)
            __im_size = __image.size
            __page["img_size"] = __im_size

            __page["scale_size"] = int(__im_size[0] * __page["scale"]), int(__im_size[1] * __page["scale"])
            __photo = ImageTk.PhotoImage(__image.resize(__page["scale_size"]))
            __page["ph"] = __photo

            if len(self._canvas.img["imgs"]) == 1:
                __page["cr_img"] = self._canvas.create_image(0, 0, anchor='nw', image=__photo, tags="photo")
            else:
                self._canvas.itemconfig(__page["cr_img"], image=__photo)
            self._canvas.config(width=__im_size[0], height=__im_size[1])
            self._canvas.configure(scrollregion=(0, 0) + __im_size)

            self._canvas.undo.append("image")

        except UnidentifiedImageError:
            messagebox.showerror('Ошибка!', 'Не удалось загузить фотографию')
        except AttributeError:
            pass

    def save_image(self):
        """ Сохраняет изображение с холста

            Возвращает:
                None

            Побочный эффект:
                Если drawQ, то сохраняет изображение через postscipt, если нет, то просто последнее изображение из
                списка изображений
        """

        __new_file = filedialog.asksaveasfilename(title="Сохранить файл",
                                                  defaultextension=".jpg",
                                                  filetypes=self._types
                                                  )

        if __new_file:
            self._canvas.saveQ = True

            __compress_window = CompressWindow(self.root)
            __compress = __compress_window.open()

            __page = self._canvas.img
            if __page["curr_img"]:
                self.append_image()
            if __page["imgs"]:
                __img = __page["imgs"][-1]
                __page["ph"] = ImageTk.PhotoImage(__img.resize((
                                                                int(__img.size[0] * 1.333333),
                                                                int(__img.size[1] * 1.333333))))
                self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])

            __bbox = None
            if len(self._canvas.obj_storage) > 1:
                self._canvas.scale(ALL, 0, 0, (1 / __page["scale"]) * 1.333333, (1 / __page["scale"]) * 1.333333)
                __bbox = self._canvas.bbox(ALL)
                self._canvas.configure(scrollregion=(0, 0, __bbox[2] - __bbox[0], __bbox[3] - __bbox[1]))
            __page["scale_size"] = tuple((int(_ * 1.333333) for _ in __page["img_size"]))
            __page["scale"] = 1.333333

            __image = None
            if len(self._canvas.obj_storage) > 1:
                if __page["imgs"]:
                    ps = self._canvas.postscript(colormode="color",
                                                 height=__bbox[3] - __bbox[1],
                                                 width=__bbox[2] - __bbox[0],
                                                 x=__bbox[0] - 5, y=__bbox[1])
                    __image = Image.open(BytesIO(ps.encode('utf-8')))
                    __image = __image.resize([_ + 4 for _ in __image.size])
                    __image = __image.crop((2, 2, __image.size[0] - 2, __image.size[1] - 2))
                else:
                    __wigth = max(800, __bbox[-2])
                    __height = max(600, __bbox[-1])
                    ps = self._canvas.postscript(colormode="color",
                                                 height=__height + 10,
                                                 width=__wigth + 10,
                                                 x=-5, y=-5
                                                 )
                    __image = Image.open(BytesIO(ps.encode('utf-8')))
            else:
                if __page["imgs"]:
                    __image = __page["imgs"][-1].resize([_ + 4 for _ in __page["img_size"]])
                    __image = __image.crop((2, 2, __image.size[0] - 2, __image.size[1] - 2))
                else:
                    __image = Image.new('RGB', (800, 600), color="white")
            __image.save(__new_file, quality=int(__compress))

            if __page["imgs"]:
                __img = __page["imgs"][-1]
                __page["ph"] = ImageTk.PhotoImage(__img.resize(__page["img_size"]))
                self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])

            __bbox = None
            if len(self._canvas.obj_storage) > 1:
                self._canvas.scale(ALL, 0, 0, 1/1.333333, 1/1.333333)
                __bbox = self._canvas.bbox(ALL)
                self._canvas.configure(scrollregion=(0, 0, __bbox[2] - __bbox[0], __bbox[3] - __bbox[1]))
            __page["scale_size"] = copy(__page["img_size"])
            __page["scale"] = 1.

    def return_image(self):
        """ Возвращает на холст предыдущее изображение из списка изображений, а текущее удаляет

            Возвращает:
                None
        """

        __page = self._canvas.img
        self._canvas.saveQ = False
        if len(__page["imgs"]) >= 2:
            del __page["imgs"][-1]
            __image = __page["imgs"][-1]
            __iw, __ih = __image.size
            __page["scale_size"] = int(__iw * __page["scale"]), int(__ih * __page["scale"])

            __page["ph"] = ImageTk.PhotoImage(__image.resize(__page["scale_size"]))
            self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])
        elif len(__page["imgs"]) == 1:
            self._canvas.saveQ = False
            __page["imgs"] = []
            __page["img_size"] = (800, 600)
            __page["ph"] = None
            __page["cr_img"] = None
            __page["curr_img"] = None

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

        __page = self._canvas.img
        if len(self._canvas.obj_storage) > 1 or __page["imgs"]:
            if event.delta > 0:
                __page["scale"] = __page["scale"] * 1.25 if __page["scale"] * 1.25 < 3.8147 else 3.8147
                self.redraw("in")
            elif event.delta < 0:
                __page["scale"] = __page["scale"] * 0.8 if __page["scale"] * 0.8 > 0.262144 else 0.262144
                self.redraw("off")

    def zoom_in(self, event):
        """ Расчитывает коэффициент масштабирования при прокрутке колеса мыши вниз

            Аргументы:
                * event: tkinter.Event - событие, по которому считывается положение курсора

            Возращает:
                None
        """

        __page = self._canvas.img
        if len(self._canvas.obj_storage) > 1 or __page["imgs"]:
            __page["scale"] = __page["scale"] * 1.25 if __page["scale"] * 1.25 < 3.8147 else 3.8147
            self.redraw("in")

    def zoom_off(self, event):
        """ Расчитывает коэффициент масштабирования при прокрутке колеса мыши вверх

            Аргументы:
                * event: tkinter.Event - событие, по которому считывается положение курсора

            Возращает:
                None
        """
        
        __page = self._canvas.img
        if len(self._canvas.obj_storage) > 1 or __page["imgs"]:
            __page["scale"] = __page["scale"] * 0.8 if __page["scale"] * 0.8 > 0.262144 else 0.262144
            self.redraw("off")

    def update_data(self, const):
        """ Обновляет данные об объектах относительно масштаба холста

            Аргументы:
                * const: float - коэффициент масштаба

            Возращает:
                None
        """
        
        for key, value in self._canvas.obj_storage.items():
            if key != 'canvas':
                for i in range(len(value['coords'])):
                    value['coords'][i] = tuple([const*x for x in value['coords'][i]])
                if 'text' in key:
                    for i in range(len(value['size'])):
                        value['size'][i] = str(round(const*int(value['size'][i])))
                    font = select_style(value['italic'][-1], value['bold'][-1], value['family'][-1], value['size'][-1])
                    self._canvas.itemconfig(key, font=font)

    def redraw(self, direction="in"):
        """ Осущесвляет масшабирование в соответствии с коэффициентом масштабирования

            Аргументы:
                * direction: str - указывает направление увеличения/уменьшения масштабирования

            Возращает:
                None

            Побочный эффект:
                Перерисовывает текущее изображение и передвигает элементы на холсте с помощью метода canvas.scale
        """

        __page = self._canvas.img
        if __page["imgs"]:
            __iw, __ih = __page["img_size"]
            __page["scale_size"] = int(__iw * __page["scale"]), int(__ih * __page["scale"])
            __image = __page["imgs"][-1]
            __page["ph"] = ImageTk.PhotoImage(__image.resize(__page["scale_size"]))
            self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])

        self._canvas.configure(scrollregion=self._canvas.bbox(ALL))

        __scroll_speed = str(float(__page["scroll_speed"]) * pow(__page["scale"], 1 / 6))
        self._canvas.configure(yscrollincrement=__scroll_speed, xscrollincrement=__scroll_speed)
        if 0.262144 < __page["scale"] < 3.8147:
            if direction == "in":
                self._canvas.scale(ALL, 0, 0, 1.25, 1.25)
                self.update_data(1.25)
            elif direction == "off":
                self._canvas.scale(ALL, 0, 0, 0.8, 0.8)
                self.update_data(0.8)


    def apply_filter_1(self, f):
        """ Применяет к изображению с холста фильтр из первой группы (DEFAULT_FILTERS_1)

            Аргументы:
                f: tkinter.StringVar - строковая переменная tkinter, в которой содержится выбранный фильтр

            Возвращает:
                None
        """

        __page = self._canvas.img
        if __page["imgs"]:
            self._canvas.saveQ = False

            __image = __page["imgs"][-1]
            __fltr = f.get()
            __image_new = None
            if __fltr == "Размытие":
                __image_new = __image.filter(ImageFilter.BLUR)
            elif __fltr == "Контур":
                __image_new = __image.filter(ImageFilter.CONTOUR)
            elif __fltr == "Резкость":
                __image_new = __image.filter(ImageFilter.EDGE_ENHANCE)
            elif __fltr == "Рельеф":
                __image_new = __image.filter(ImageFilter.EMBOSS)
            elif __fltr == "Выделение краев":
                __image_new = __image.filter(ImageFilter.FIND_EDGES)
            elif __fltr == "Сглаживание":
                __image_new = __image.filter(ImageFilter.SMOOTH)
            __page["imgs"].append(__image_new)
            __page["ph"] = ImageTk.PhotoImage(__image_new.resize(__page["scale_size"]))
            self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])

            self._canvas.undo.append("image")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")

    def apply_filter_2(self, f, per, event=None):
        """ Применяет к изображению с холста фильтр из второй группы (DEFAULT_FILTERS_2)

            Аргументы:
                f: tkinter.StringVar - строковая переменная tkinter, в которой содержится выбранный фильтр
                per: tkinter.Scale - ползунок tkinter, в котором содержится процент применения фильтра

            Возвращает:
                None
        """

        __page = self._canvas.img
        if __page["imgs"]:
            __percent = float(per.get()) / 100
            __fltr = f.get()
            __image = __page["imgs"][-1]
            __image_new = None
            if __fltr == "Насыщенность":
                __image_new = ImageEnhance.Color(__image).enhance(__percent)
            elif __fltr == "Контрастность":
                __image_new = ImageEnhance.Contrast(__image).enhance(__percent)
            elif __fltr == "Яркость":
                __image_new = ImageEnhance.Brightness(__image).enhance(__percent)
            elif __fltr == "Острота":
                __image_new = ImageEnhance.Sharpness(__image).enhance(__percent)
            else:
                pass
            __page["curr_img"] = __image_new
            __page["ph"] = ImageTk.PhotoImage(__image_new.resize(__page["scale_size"]))
            self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")

    def apply_filter_3(self, f):
        """ Применяет к изображению с холста фильтр из третьей группы (DEFAULT_FILTERS_3)

            Аргументы:
                f: tkinter.StringVar - строковая переменная tkinter, в которой содержится выбранный фильтр

            Возвращает:
                None
        """

        __page = self._canvas.img
        if __page["imgs"]:
            self._canvas.saveQ = False

            __fltr = f.get()
            __w, __h = __page["img_size"][0], __page["img_size"][1]
            __image = __page["imgs"][-1]
            __mode = None
            if __image.mode != "RGB":
                __mode = __image.mode
                __image = __image.convert("RGB")
            __image_new = None
            if __fltr == "Негатив":
                __image_new = ImageOps.invert(__image)
            elif __fltr == "Оттенки серого":
                __image_new = ImageOps.grayscale(__image)
            elif __fltr == "Соляризация":
                __image_new = ImageOps.solarize(__image)
            else:
                pass
            if __mode:
                __image_new = __image.convert(__mode)
            __page["imgs"].append(__image_new)
            __page["ph"] = ImageTk.PhotoImage(__image_new.resize(__page["scale_size"]))
            self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])

            self._canvas.undo.append("image")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")

    def apply_filter_4(self):
        """ Применяет к изображению с холста ванильный-фильтр

            Возвращает:
                None
        """

        __page = self._canvas.img
        if __page["imgs"]:
            self._canvas.saveQ = False

            try:
                __image = __page['imgs'][-1]

                __mode = None
                if __image.mode != 'RGB':
                    __mode = __image.mode
                    __image = __image.convert("RGB")

                __colors = __image.split()
                __sample = choices(__colors, k=len(__colors))
                while __sample[0] == __sample[1] == __sample[2]:
                    __sample = choices(__colors, k=len(__colors))
                __image_new = Image.merge(__image.mode, __sample)

                if __mode:
                    __image_new = __image.convert(__mode)

                __page["imgs"].append(__image_new)
                __page["ph"] = ImageTk.PhotoImage(__image_new.resize(__page["scale_size"]))
                self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])

                self._canvas.undo.append("image")
            except ValueError:
                messagebox.showerror("Ошибка!", "Применить фильтр не удалось")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")

    def change_layers(self, red, green, blue, event=None):
        """ Изменяет насыщенность каждого слоя в отдельности

            Аргументы:
                r: tkinter.Scale - ползунок tkinter, в котором содержится значение для красного слоя
                g: tkinter.Scale - ползунок tkinter, в котором содержится значение для зеленого слоя
                b tkinter.Scale - ползунок tkinter, в котором содержится значение для синего слоя

            Возвращает:
                None
        """

        __page = self._canvas.img
        if __page["imgs"]:
            try:
                __image = __page["imgs"][-1]
                __mode = None
                if __image.mode != 'RGB':
                    __mode = __image.mode
                    __image = __image.convert("RGB")
                __r_value = float(red.get()) / 100.
                __g_value = float(green.get()) / 100.
                __b_value = float(blue.get()) / 100.

                __layers = __image.split()
                __r_layer = __layers[0].point(lambda i: i * __r_value)
                __g_layer = __layers[1].point(lambda i: i * __g_value)
                __b_layer = __layers[2].point(lambda i: i * __b_value)

                __image_new = Image.merge('RGB', (__r_layer, __g_layer, __b_layer))

                if __mode:
                    __image_new = __image.convert(__mode)

                __page["curr_img"] = __image_new
                __page["ph"] = ImageTk.PhotoImage(__image_new.resize(__page["scale_size"]))
                self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])

            except ValueError:
                messagebox.showerror("Ошибка!", "Применить фильтр не удалось")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")

    def normalize_image(self):
        """ Нормализует изображение

            Возвращает:
                None
        """

        __page = self._canvas.img
        if __page["imgs"]:
            try:
                self._canvas.saveQ = False

                __image = __page["imgs"][-1]
                __mode = None
                if __image.mode != 'RGB':
                    __mode = __image.mode
                    __image = __image.convert("RGB")
                __image_new = ImageOps.equalize(__image)
                if __mode:
                    __image_new = __image.convert(__mode)

                __page["imgs"].append(__image_new)
                __page["ph"] = ImageTk.PhotoImage(__image_new.resize(__page["scale_size"]))
                self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])

                self._canvas.undo.append("image")

            except ValueError:
                messagebox.showerror("Ошибка!", "Применить фильтр не удалось")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")

    def append_image(self):
        """ Добавляет изображение в список изображений после прокрутки Scale'ов

            Возвращает:
                None

            Побочные действия:
                Очищает _canvas.img["curr_img"]
        """

        __page = self._canvas.img
        if __page["curr_img"]:
            self._canvas.saveQ = False

            __page["imgs"].append(copy(__page["curr_img"]))
            __page["curr_img"] = None

            self._canvas.undo.append("image")

    def reflect_image(self, direction):
        """ Отражает изображение по горизонтали или по вертикали.

            Аргументы:
                direction: String - строка, в которой содержится выбранный фильтр
            Возвращает:
                None
        """

        __page = self._canvas.img
        if __page["imgs"]:
            if len(self._canvas.obj_storage) == 1:
                self._canvas.saveQ = False

                __image = __page["imgs"][-1]
                __mode = None
                if __image.mode != 'RGB':
                    __mode = __image.mode
                    __image = __image.convert("RGB")

                if direction == "horizontal":
                    __image_new = ImageOps.mirror(__image)
                elif direction == "vertical":
                    __image_new = ImageOps.flip(__image)
                else:
                    __image_new = __image

                if __mode:
                    __image_new = __image.convert(__mode)

                __page["imgs"].append(__image_new)
                __page["ph"] = ImageTk.PhotoImage(__image_new.resize(__page["scale_size"]))
                self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])

                self._canvas.undo.append("image")

            else:
                messagebox.showerror("Ошибка!", "Изображение можно отразить только в том случае, если на нем ничего "
                                                "не нарисовано")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")

    def rotate_image(self, direction):
        """ Поворачивает изображение по часовой или против часовой стрелки.

            Аргументы:
                    direction: String - строка, в которой содержится выбранный фильтр
            Возвращает:
                    None
        """

        __page = self._canvas.img
        if __page["imgs"]:
            if len(self._canvas.obj_storage) == 1:
                self._canvas.saveQ = False

                __image = __page["imgs"][-1]
                __mode = None
                if __image.mode != 'RGB':
                    __mode = __image.mode
                    __image = __image.convert("RGB")

                if direction == "90":
                    __image_new = __image.transpose(Image.ROTATE_90)
                elif direction == "-90":
                    __image_new = __image.transpose(Image.ROTATE_270)
                else:
                    __image_new = __image

                if __mode:
                    __image_new = __image.convert(__mode)

                __page["imgs"].append(__image_new)
                __page["scale_size"] = __page["scale_size"][::-1]
                __page["img_size"] = __page["img_size"][::-1]
                self._canvas.configure(scrollregion=(0, 0) + __page["scale_size"])
                __page["ph"] = ImageTk.PhotoImage(__image_new.resize(__page["scale_size"]))
                self._canvas.itemconfig(__page["cr_img"], image=__page["ph"])

                self._canvas.undo.append("image")

            else:
                messagebox.showerror("Ошибка!", "Изображение можно отразить только в том случае, если на нем ничего "
                                                "не нарисовано")
        else:
            messagebox.showwarning("Внимание!", "Сначала загрузите изображение")
