# Импротированные модули
from ._basic import *
from ._custom_windows import TextSettingsWindow
from tkinter import *
from math import floor


class Draw:
    """ Draw - логика работы с графическими примитивами

        Аргументы:
            * root: tkinter.Tk - главное окно
            * event: tkinter.Event - событие, по которому считывается положение курсора
            * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором происходит отрисовка

        Методы:
            * point(*, size: int of float = DEFAULT_SIZE, color: str = DEFAULT_FIRST_COLOR, debug_mode: bool = False) -> None
            * oval(*, thickness: int or float = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * line(*, thickness: int of float = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR, arrow: bool = False) -> None
            * polygon(self, *, thickness: int or float = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * rectangle(*, thickness: int or float = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * text_creation(self) -> None
            * coordinate_plane(*, thickness: int or float = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None
            * move(self) -> None
            * fill_objects(self, *, color: str = DEFAULT_CHANGE_COLOR) -> None
            * thickness_objects(self, *, thickness: int or float = DEFAULT_THICKNESS) -> None
            * outline_color_objects(self, *, color: str = DEFAULT_CHANGE_COLOR) -> None
            * quick_eraser(self) -> None
            * on_canvas(self) -> None
            * undo(self) -> None
    """

    def __init__(self, root, event, canvas):
        self._root = root
        self._event = event
        self._canvas = canvas

    def point(self,
              *,
              size,
              color,
              debug_mode=False):
        """ Рисует точку на месте курсора

            Аргументы:
                ** size: int or float - размер точки (отрезок)
                ** color: str - цвет точки (отрезок)
                ** debug_mode: bool - режим отладчика

            Возвращает:
                None

            Побочный эффект:
                Отрисовка точки (отрезок) на canvas'e (слое)
        """

        event, canvas = self._event, self._canvas
        x1, y1 = canvas.canvasx(event.x), canvas.canvasy(event.y)

        if str(event.type) == 'ButtonRelease' and canvas.line_sequences and canvas.hover:
            self._canvas.undo.append("graphic")
            self._canvas.saveQ = False
            canvas.old_point = None
            tag = f'brush{len(canvas.obj_storage) + 1}'
            x_min, y_min, x_max, y_max = transform_line_sequence(canvas.line_sequences)
            canvas.obj_storage[tag] = {'coords': [(x_min-size, y_min-size, x_max+size, y_max+size)], 'color': [color], 'size': [size], 'modifications': ['creation']}
            canvas.modified_objs.append(tag)
            if debug_mode:
                canvas.create_rectangle(x_min-size, y_min-size, x_max+size, y_max+size, dash=(5, 3), tags=tag)
            canvas.addtag_enclosed(tag, x_min-size, y_min-size, x_max+size, y_max+size)
            canvas.line_sequences = []
        elif str(event.type) == 'Motion' and canvas.hover:
            if canvas.old_point:
                x2, y2 = canvas.old_point
                canvas.create_line(x1, y1, x2, y2, width=size, fill=color, smooth=TRUE, capstyle=ROUND)
                canvas.line_sequences.append([(x1, y1), (x2, y2)])
            canvas.old_point = x1, y1

    def line(self,
             *,
             thickness,
             color,
             arrow=False):
        """ Рисует линию по заданным точкам

             Аргументы:
                ** thickness: int or float - жирность линии (отрезка)
                ** color: str - цвет линии (отрезка)
                ** arrow: bool - нужно ли делать стрелку на конце линии

            Возвращает:
                None

            Побочный эффект:
                Отрисовка линии по заданным точкам на canvas'e
        """

        event, canvas = self._event, self._canvas
        new_point = canvas.canvasx(event.x), canvas.canvasy(event.y)

        if str(event.type) == 'ButtonPress' and canvas.hover:
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point and canvas.hover:
            self._canvas.undo.append("graphic")
            self._canvas.saveQ = False
            tag = f'line{len(canvas.obj_storage) + 1}'
            x2, y2 = canvas.old_point
            x1, y1 = transform_line_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            line = canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color, smooth=TRUE, capstyle=ROUND, tags=tag)
            if arrow:
                canvas.itemconfig(line, arrow=FIRST)
            canvas.obj_storage[tag] = {'coords': [(x1, y1, x2, y2)], 'color': [color], 'thickness': [thickness], 'modifications': ['creation']}
            canvas.modified_objs.append(tag)
            canvas.delete(canvas.obj_line)
        elif str(event.type) == 'Motion' and canvas.old_point and canvas.hover:
            x2, y2 = canvas.old_point
            x1, y1 = transform_line_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            line = canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color, smooth=TRUE, capstyle=ROUND)

            if arrow:
                canvas.itemconfig(line, arrow=FIRST)

            if canvas.obj_line:
                canvas.delete(canvas.obj_line)

            canvas.obj_line = line

    def oval(self,
             *,
             thickness,
             bgcolor,
             outcolor):
        """ Рисует эллипс по заданным точкам

            Аргументы:
                ** thickness: int or float - жирность обводки эллипса
                ** bgcolor: str - цвет заливки эллипса
                ** outcolor: str - цвет обводки эллипса

            Возвращает:
                None

            Побочный эффект:
                Отрисовка эллипса по заданным точкам на canvas'е
        """

        event, canvas = self._event, self._canvas
        new_point = canvas.canvasx(event.x), canvas.canvasy(event.y)

        if str(event.type) == 'ButtonPress' and canvas.hover:
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point and canvas.hover:
            self._canvas.undo.append("graphic")
            self._canvas.saveQ = False
            tag = f'oval{len(canvas.obj_storage) + 1}'
            x1, y1 = transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor, tags=tag)
            canvas.obj_storage[tag] = {'coords': [(x1, y1, x2, y2)], 'bgcolor': [bgcolor], 'outcolor': [outcolor], 'thickness': [thickness], 'modifications': ['creation']}
            canvas.modified_objs.append(tag)
            canvas.delete(canvas.obj_oval)
        elif str(event.type) == 'Motion' and canvas.old_point and canvas.hover:
            x1, y1 = transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            oval = canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)

            if canvas.obj_oval:
                canvas.delete(canvas.obj_oval)

            canvas.obj_oval = oval

    def rectangle(self,
                  *,
                  thickness,
                  bgcolor,
                  outcolor):
        """ Рисует прямоугольник по заданным точкам

            Аргументы:
                ** thickness: int of float - жирность обводки прямоугольник
                ** bgcolor: str - цвет заливки прямоугольник
                ** outcolor: str - цвет обводки прямоугольник

            Возвращает:
                None

            Побочный эффект:
                Отрисовка прямоугольника по заданным точкам на canvas'е
        """

        event, canvas = self._event, self._canvas
        new_point = canvas.canvasx(event.x), canvas.canvasy(event.y)

        if str(event.type) == 'ButtonPress' and canvas.hover:
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point and canvas.hover:
            self._canvas.undo.append("graphic")
            self._canvas.saveQ = False
            tag = f'rectangle{len(canvas.obj_storage)+1}'
            x1, y1 = transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            canvas.create_rectangle(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor, tags=tag)
            canvas.obj_storage[tag] = {'coords': [(x1, y1, x2, y2)], 'bgcolor': [bgcolor], 'outcolor': [outcolor], 'thickness': [thickness], 'modifications': ['creation']}
            canvas.modified_objs.append(tag)
            canvas.delete(canvas.obj_rectangle)
        elif str(event.type) == 'Motion' and canvas.old_point and canvas.hover:
            x1, y1 = transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            rect = canvas.create_rectangle(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)

            if canvas.obj_rectangle:
                canvas.delete(canvas.obj_rectangle)

            canvas.obj_rectangle = rect

    def polygon(self,
                *,
                thickness,
                bgcolor,
                outcolor):
        """ Рисует многоугольник по заданным точкам

            Аргументы:
                ** thickness: int or float - жирность обводки многоугольника
                ** bgcolor: str - цвет заливки многоугольника
                ** outcolor: str - цвет обводки многоугольника

            Возвращает:
                None

            Побочный эффект:
                Отрисовка многоугольника по заданным точкам на canvas'e
        """

        event, canvas = self._event, self._canvas
        new_point = canvas.canvasx(event.x), canvas.canvasy(event.y)

        if str(event.type) == 'ButtonPress' and not canvas.old_point and canvas.hover:
            canvas.start_point = new_point
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point and canvas.hover:
            x2, y2 = canvas.old_point
            x1, y1 = transform_line_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            canvas.create_line(x1, y1, x2, y2, width=thickness, fill=outcolor, smooth=TRUE, capstyle=ROUND, tags='temp_line')
            canvas.delete(canvas.obj_line)
            if x1-10 < canvas.start_point[0] < x1+10 and y1-10 < canvas.start_point[1] < y1+10:
                self._canvas.undo.append("graphic")
                self._canvas.saveQ = False
                tag = f'polygon{len(canvas.obj_storage) + 1}'
                x1, y1 = canvas.start_point
                x_delta, y_delta = abs(x1-canvas.start_point[0]), abs(y1-canvas.start_point[1])
                canvas.line_sequences.append([(x2, y2), (x1+x_delta, y1+y_delta)])
                canvas.old_point, canvas.start_point = None, None
                polygon = canvas.create_polygon(*flatten(canvas.line_sequences), width=thickness, fill=bgcolor, outline=outcolor, tags=tag)
                canvas.line_sequences = []
                canvas.obj_storage[tag] = {'coords': [canvas.coords(polygon)], 'bgcolor': [bgcolor], 'outcolor': [outcolor], 'thickness': [thickness], 'modifications': ['creation']}
                canvas.modified_objs.append(tag)
                canvas.delete('temp_line')
            else:
                canvas.line_sequences.append([(x2, y2), (x1, y1)])
                canvas.old_point = x1, y1
        elif str(event.type) == 'Motion' and canvas.old_point and canvas.hover:
            x2, y2 = canvas.old_point
            x1, y1 = transform_line_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            line = canvas.create_line(x1, y1, x2, y2, width=thickness, fill=outcolor, smooth=TRUE, capstyle=ROUND)

            if canvas.obj_line:
                canvas.delete(canvas.obj_line)

            canvas.obj_line = line

    def text_creation(self):
        """ Создаёт и редактируем текст на canavas'e (слое)

            Возвращает:
                None

            Побочный эффект:
                Вызывает модальное окно с настстройками текста, создаёт и редактирует текст на canvas'e
        """

        event, canvas, root = self._event, self._canvas, self._root
        canvas.obj_tag = detect_object(event, canvas)

        if canvas.hover:
            if not canvas.obj_tag:
                tag = f'text{len(canvas.obj_storage) + 1}'
                window = TextSettingsWindow(root, text='', family='Arial', size='12', italic=False, bold=False, color='black')
                data = window.get_data()
                x, y = event.x, event.y
                text, color, family, size, italicB, boldB = data
                if text != '':
                    canvas.create_text(x, y, text=text, fill=color, tags=tag)

                    font = select_style(italicB, boldB, family, size)
                    canvas.itemconfig(tag, font=font)
                    canvas.obj_storage[tag] = {'coords': [canvas.bbox(tag)],
                                               'text': [text],
                                               'family': [family],
                                               'size': [size],
                                               'color': [color],
                                               'italic': [italicB],
                                               'bold': [boldB],
                                               'modifications': ['creation']}
                    canvas.modified_objs.append(tag)

            elif 'text' in canvas.obj_tag:
                data = tuple(canvas.obj_storage[canvas.obj_tag].values())[1:-1]
                formated_data = [item[-1] for item in data]

                text, family, size, color, italicB, boldB = formated_data
                window = TextSettingsWindow(root, text=text, family=family, size=size, italic=italicB, bold=boldB, color=color)

                data = window.get_data()
                text, color, family, size, italicB, boldB = data

                font = select_style(italicB, boldB, family, size)
                canvas.itemconfig(canvas.obj_tag, text=text, font=font, fill=color)

                names_values = ['text', 'color', 'family', 'size', 'italic', 'bold', 'modifications', 'coords']
                data_values = list(data)
                data_values.append('text_editing')
                data_values.append(canvas.bbox(canvas.obj_tag))
                history_data = {names_values[i]: data_values[i] for i in range(len(names_values))}

                for label, value in history_data.items():
                    canvas.obj_storage[canvas.obj_tag][label].append(value)

                canvas.modified_objs.append(canvas.obj_tag)
            self._canvas.undo.append("graphic")
            self._canvas.saveQ = False

    def coordinate_plane(self,
                         *,
                         thickness,
                         color):
        """ Создаёт двумерную координатную плоскость

            Аргументы:
                ** thickness: int or float - жирность осей
                ** color: str - цвет осей

            Возвращает:
                None

            Побочный эффект:
                Отрисовка двумерной координатной плоскости на canvas'е (слое)
        """

        event, canvas = self._event, self._canvas
        new_point = canvas.canvasx(event.x), canvas.canvasy(event.y)

        if str(event.type) == 'ButtonPress' and canvas.hover:
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point and canvas.hover:
            self._canvas.undo.append("graphic")
            self._canvas.saveQ = False

            tag = f'plane{len(canvas.obj_storage)+1}'
            x1, y1 = transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            canvas.create_line(x1, y2+(y1-y2)/2, x2, y2+(y1-y2)/2, width=thickness, fill=color, arrow=FIRST, tags=tag)
            canvas.create_line(x2+(x1-x2)/2, y1, x2+(x1-x2)/2, y2, width=thickness, fill=color, arrow=LAST, tags=tag)
            canvas.obj_storage[tag] = {'coords': [canvas.bbox(tag)], 'color': [color], 'thickness': [thickness], 'modifications': ['creation']}
            canvas.addtag_enclosed(tag, x1+thickness, y1+thickness, x2-thickness, y2-thickness)
            canvas.modified_objs.append(tag)
            canvas.delete(canvas.obj_horizontal_axis)
            canvas.delete(canvas.obj_vertical_axis)
            canvas.delete(canvas.obj_rectangle)
        elif str(event.type) == 'Motion' and canvas.old_point and canvas.hover:
            x1, y1 = transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            horizontal_axis = canvas.create_line(x1, y2+(y1-y2)/2, x2, y2+(y1-y2)/2, width=thickness, fill=color, arrow=FIRST)
            vertical_axis = canvas.create_line(x2+(x1-x2)/2, y1, x2+(x1-x2)/2, y2, width=thickness, fil=color, arrow=LAST)
            rect = canvas.create_rectangle(x1, y1, x2, y2, width=1, dash=(5, 3))

            if canvas.obj_rectangle and canvas.obj_horizontal_axis and canvas.obj_vertical_axis:
                canvas.delete(canvas.obj_horizontal_axis)
                canvas.delete(canvas.obj_vertical_axis)
                canvas.delete(canvas.obj_rectangle)

            canvas.obj_rectangle = rect
            canvas.obj_horizontal_axis = horizontal_axis
            canvas.obj_vertical_axis = vertical_axis

    def move(self):
        """ Двигает объекты на canvas'e (слое)

            Возвращает:
                None

            Побочный эффект:
                Двигает объект на слое (canvas'e) и перезаписывает его координаты
        """

        event, canvas = self._event, self._canvas

        if str(event.type) == 'ButtonPress' and canvas.hover:
            canvas.obj_tag = detect_object(event, canvas)
        elif str(event.type) == 'ButtonRelease' and canvas.obj_tag and canvas.hover:
            self._canvas.undo.append("graphic")
            self._canvas.saveQ = False

            if 'brush' in canvas.obj_tag:
                raw_points = [tuple(map(lambda x: floor(x), canvas.coords(obj))) for obj in canvas.find_withtag(canvas.obj_tag)]
                points_storage = list(map(lambda sublist: [sublist[i:i+2] for i in range(0, len(sublist), 2)], raw_points))
                x_min, y_min, x_max, y_max = transform_line_sequence(points_storage)
                canvas.obj_storage[canvas.obj_tag]['coords'].append((x_min, y_min, x_max, y_max))
            elif 'text' in canvas.obj_tag or 'plane' in canvas.obj_tag:
                canvas.obj_storage[canvas.obj_tag]['coords'].append(canvas.bbox(canvas.obj_tag))
            else:
                canvas.obj_storage[canvas.obj_tag]['coords'].append(canvas.coords(canvas.obj_tag))
            canvas.obj_storage[canvas.obj_tag]['modifications'].append('move')
            canvas.modified_objs.append(canvas.obj_tag)
            canvas.obj_tag = None
        elif str(event.type) == 'Motion' and canvas.obj_tag and canvas.hover:
            coords = canvas.bbox(canvas.obj_tag) if 'text' in canvas.obj_tag else canvas.coords(canvas.obj_tag)[0:4]
            x1, y1, x2, y2 = coords
            obj_center_x, obj_center_y = (x1+x2)/2, (y1+y2)/2
            mouse_x, mouse_y = canvas.canvasx(event.x), canvas.canvasy(event.y)

            move_x, move_y = mouse_x-obj_center_x, mouse_y-obj_center_y

            canvas.move(canvas.obj_tag, move_x, move_y)

    def fill_objects(self,
                     *,
                     color):
        """ Заливка объекта на canvas'е (слое)

            Аргументы:
                ** color: str - цвет, в который будет перекрашен объект

            Возвращает:
                None

            Побочный эффект:
                Перекрашивает объект в цвет color на canvas'e (слое)
        """

        event, canvas = self._event, self._canvas
        canvas.obj_tag = detect_object(event, canvas)

        if canvas.obj_tag and canvas.hover:
            if 'brush' in canvas.obj_tag or 'plane' in canvas.obj_tag:
                for member in canvas.find_withtag(canvas.obj_tag):
                     canvas.itemconfig(member, fill=color)
                canvas.obj_storage[canvas.obj_tag]['color'].append(color)
                canvas.obj_storage[canvas.obj_tag]['modifications'].append('fill')
                canvas.modified_objs.append(canvas.obj_tag)
            elif 'text' not in canvas.obj_tag:
                canvas.itemconfig(canvas.obj_tag, fill=color)
                color_label = 'color' if 'line' in canvas.obj_tag else 'bgcolor'
                canvas.obj_storage[canvas.obj_tag][color_label].append(color)
                canvas.obj_storage[canvas.obj_tag]['modifications'].append('fill')
                canvas.modified_objs.append(canvas.obj_tag)
        elif canvas.hover:
            canvas['background'] = color
            canvas.modified_objs.append('canvas')
            canvas.obj_storage['canvas']['color'].append(color)
        canvas.undo.append("graphic")

    def thickness_objects(self,
                          *,
                          thickness):
        """ Толщина объекта на canvas'е (слое)

            Аргументы:
                ** thickness: int or float - жирность обводки объекта

            Возвращает:
                None

            Побочный эффект:
                Изменяет жирность обводки объекта
        """

        event, canvas = self._event, self._canvas
        canvas.obj_tag = detect_object(event, canvas)

        if canvas.obj_tag:
            canvas.undo.append("graphic")
            if 'brush' in canvas.obj_tag or 'plane' in canvas.obj_tag:
                thick_label = 'size' if 'brush' in canvas.obj_tag else 'thickness'
                for member in canvas.find_withtag(canvas.obj_tag):
                    canvas.itemconfig(member, width=thickness)
                canvas.obj_storage[canvas.obj_tag][thick_label].append(thickness)
                canvas.obj_storage[canvas.obj_tag]['modifications'].append('thickness')
                canvas.modified_objs.append(canvas.obj_tag)
            elif 'text' not in canvas.obj_tag:
                canvas.itemconfig(canvas.obj_tag, width=thickness)
                canvas.obj_storage[canvas.obj_tag]['thickness'].append(thickness)
                canvas.obj_storage[canvas.obj_tag]['modifications'].append('thickness')
                canvas.modified_objs.append(canvas.obj_tag)

    def outline_color_objects(self,
                              *,
                              color):
        """ Цвет обводки объекта на canvas'е (слое)

            Аргументы:
                ** color: str - цвет, в который будет перекрашена обводка объекта

            Возвращает:
                None

            Побочный эффект:
                Изменяет цвет обводки объекта
        """

        event, canvas = self._event, self._canvas
        canvas.obj_tag = detect_object(event, canvas)
        valiable_objs = ['rectangle', 'oval', 'polygon']

        if canvas.obj_tag:
            canvas.undo.append("graphic")
            if any([obj in canvas.obj_tag for obj in valiable_objs]):
                canvas.modified_objs.append(canvas.obj_tag)
                obj = canvas.find_withtag(canvas.obj_tag)
                canvas.itemconfig(obj, outline=color)
                canvas.obj_storage[canvas.obj_tag]['outcolor'].append(color)
                canvas.obj_storage[canvas.obj_tag]['modifications'].append('outcolor')

    def quick_eraser(self):
        """ 'Быстрый' ластик

            Возвращает:
                None

            Побочный эффект:
                За одно касание удаляет графический примитив
        """

        event, canvas = self._event, self._canvas

        canvas.obj_tag = detect_object(event, canvas)
        if canvas.obj_tag:
            canvas.undo.append("graphic")
            canvas.modified_objs = [obj for obj in canvas.modified_objs if obj != canvas.obj_tag]
            del canvas.obj_storage[canvas.obj_tag]
        canvas.delete(canvas.obj_tag)

    def on_canvas(self):
        """ Проверяет находится ли курсор на canvas'е (слое) или нет

            Возвращает:
                None

            Побочный эффект:
               Опредлеяет находится ли курсор на canvas'е (слое) или нет и записывет результат в поле hover
        """

        event, canvas = self._event, self._canvas
        if str(event.type) == 'Leave':
            canvas.hover = False
        elif str(event.type) == 'Enter':
            canvas.hover = True

    def undo(self):
        """ Отменяет действия, который были сделаны с графическими примитивами

            Возвращает:
                None

            Побочный эффект:
               Отменяет все действия, которые произвёл пользователь с графическими примитивами
        """

        canvas = self._canvas
        storage = canvas.obj_storage

        if storage and canvas.modified_objs:
            last_modified_obj = canvas.modified_objs[-1]
            if last_modified_obj == 'canvas' and len(storage[last_modified_obj]['color']) > 1:
                canvas['background'] = storage[last_modified_obj]['color'][-2]
                del storage[last_modified_obj]['color'][-1]
            elif storage[last_modified_obj]['modifications'][-1] == 'fill':
                if 'brush' in last_modified_obj or 'plane' in last_modified_obj:
                    for member in canvas.find_withtag(last_modified_obj):
                        canvas.itemconfig(member, fill=storage[last_modified_obj]['color'][-2])
                    del storage[last_modified_obj]['color'][-1]
                else:
                    color = 'color' if 'line' in last_modified_obj else 'bgcolor'
                    canvas.itemconfig(last_modified_obj, fill=storage[last_modified_obj][color][-2])
                    del storage[last_modified_obj][color][-1]
                del storage[last_modified_obj]['modifications'][-1]
            elif storage[last_modified_obj]['modifications'][-1] == 'creation':
                canvas.delete(last_modified_obj)
                del storage[last_modified_obj]
            elif storage[last_modified_obj]['modifications'][-1] == 'move':
                if 'brush' in last_modified_obj or 'text' in last_modified_obj or 'plane' in last_modified_obj:
                    x1, y1 = storage[last_modified_obj]['coords'][-1][-2:]
                    x2, y2 = storage[last_modified_obj]['coords'][-2][-2:]
                    canvas.move(last_modified_obj, x2-x1, y2-y1)
                else:
                    canvas.coords(last_modified_obj, *storage[last_modified_obj]['coords'][-2])
                del storage[last_modified_obj]['coords'][-1]
                del storage[last_modified_obj]['modifications'][-1]

            elif storage[last_modified_obj]['modifications'][-1] == 'thickness':
                if 'brush' in last_modified_obj or 'plane' in last_modified_obj:
                    thick_label = 'size' if 'brush' in canvas.obj_tag else 'thickness'  # TODO: тут Егор что-то исправил
                    for member in canvas.find_withtag(last_modified_obj):
                        canvas.itemconfig(member, width=storage[last_modified_obj][thick_label][-2])
                    del storage[last_modified_obj][thick_label][-1]
                else:
                    canvas.itemconfig(last_modified_obj, width=storage[last_modified_obj]['thickness'][-2])
                    del storage[last_modified_obj]['thickness'][-2]
                del storage[last_modified_obj]['modifications'][-1]
            elif storage[last_modified_obj]['modifications'][-1] == 'outcolor':
                canvas.itemconfig(last_modified_obj, outline=storage[last_modified_obj]['outcolor'][-2])
                del storage[last_modified_obj]['outcolor'][-1]
                del storage[last_modified_obj]['modifications'][-1]
            elif storage[last_modified_obj]['modifications'][-1] == 'text_editing':
                data = list(storage[last_modified_obj].values())[1:-1]
                previous_data = (params[-2] for params in data)
                text, family, size, color, italicB, boldB = previous_data
                values_label = ['text', 'family', 'size', 'color', 'italic', 'bold']
                font = select_style(italicB, boldB, family, size)
                canvas.itemconfig(last_modified_obj, text=text, font=font, fill=color)
                for key, value in storage[last_modified_obj].items():
                    if key in values_label:
                        del value[-1]
                del storage[last_modified_obj]['modifications'][-1]

            del canvas.modified_objs[-1]