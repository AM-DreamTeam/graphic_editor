# Импротированные модули
from ._basic import *
from tkinter import *
from math import atan2, sin, cos, floor


class Draw:
    """ Draw - логика работы с графическими примитивами

        Аргументы:
            * event: tkinter.Event - событие, по которому считывается положение курсора
            * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором происходит отрисовка

        Методы:
            * point(*, size: int of float = DEFAULT_SIZE, color: str = DEFAULT_FIRST_COLOR, debug_mode: bool = False) -> None
            * oval(*, thickness: int or float = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * line(*, thickness: int of float = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * polygon(self, *, thickness: int or float = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * rectangle(*, thickness: int or float = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * move(*, mouse_speed: int = DEFAULT_MOUSE_SPEED) -> None
            * fill_objects(self, *, color: str = DEFAULT_CHANGE_COLOR) -> None
            * thickness_objects(self, *, thickness: int or float = DEFAULT_THICKNESS) -> None
            * outline_color_objects(self, *, color: str = DEFAULT_CHANGE_COLOR) -> None
            * quick_eraser(self) -> None
            * on_canvas(self) -> None
            * undo(self) -> None
    """

    def __init__(self, event, canvas):
        self._event = event
        self._canvas = canvas

    def point(self,
              *,
              size,
              color,
              debug_mode = False):
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
             color):
        """ Рисует линию по заданным точкам

             Аргументы:
                ** thickness: int or float - жирность линии (отрезка)
                ** color: str - цвет линии (отрезка)

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
            tag = f'line{len(canvas.obj_storage) + 1}'
            x2, y2 = canvas.old_point
            x1, y1 = transform_line_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color, smooth=TRUE, capstyle=ROUND, tags=tag)
            canvas.obj_storage[tag] = {'coords': [(x1, y1, x2, y2)], 'color': [color], 'thickness': [thickness], 'modifications': ['creation']}
            canvas.modified_objs.append(tag)
            canvas.delete(canvas.obj_line)
        elif str(event.type) == 'Motion' and canvas.old_point and canvas.hover:
            x2, y2 = canvas.old_point
            x1, y1 = transform_line_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            line = canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color, smooth=TRUE, capstyle=ROUND)

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
            canvas.old_point = event.x, event.y
        elif str(event.type) == 'ButtonRelease' and canvas.old_point and canvas.hover:
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

    def move(self,
             *,
             mouse_speed):
        """ Двигает объекты на canvas'e (слое)

            Аргументы:
                ** mouse_speed: int - скорость передвижения объектов (скорость мыши) на слое (canvas'e)

            Возвращает:
                None

            Побочный эффект:
                Двигает объект на слое (canvas'e) и перезаписывает его координаты
        """

        event, canvas = self._event, self._canvas

        if str(event.type) == 'ButtonPress' and canvas.hover:
            canvas.obj_tag = detect_object(event, canvas)
        elif str(event.type) == 'ButtonRelease' and canvas.obj_tag and canvas.hover:
            if 'brush' in canvas.obj_tag:
                raw_points = [tuple(map(lambda x: floor(x), canvas.coords(obj))) for obj in canvas.find_withtag(canvas.obj_tag)]
                points_storage = list(map(lambda sublist: [sublist[i:i+2] for i in range(0, len(sublist), 2)], raw_points))
                x_min, y_min, x_max, y_max = transform_line_sequence(points_storage)
                canvas.obj_storage[canvas.obj_tag]['coords'].append((x_min, y_min, x_max, y_max))
            else:
                canvas.obj_storage[canvas.obj_tag]['coords'].append(canvas.coords(canvas.obj_tag))
            canvas.obj_storage[canvas.obj_tag]['modifications'].append('move')
            canvas.modified_objs.append(canvas.obj_tag)
            canvas.obj_tag = None
        elif str(event.type) == 'Motion' and canvas.obj_tag and canvas.hover:
            x1, y1, x2, y2 = canvas.coords(canvas.obj_tag)[0:4]
            obj_center_x, obj_center_y = (x1+x2)/2, (y1+y2)/2
            mouse_x, mouse_y = event.x, event.y

            move_x, move_y = mouse_x-obj_center_x, mouse_y-obj_center_y
            theta = atan2(move_y, move_x)
            x, y = mouse_speed*cos(theta), mouse_speed*sin(theta)

            canvas.move(canvas.obj_tag, x, y)

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

        if canvas.obj_tag:
            canvas.modified_objs.append(canvas.obj_tag)
            if 'brush' in canvas.obj_tag:
                for member in canvas.find_withtag(canvas.obj_tag):
                     canvas.itemconfig(member, fill=color)
                canvas.obj_storage[canvas.obj_tag]['color'].append(color)
            else:
                obj = canvas.find_withtag(canvas.obj_tag)
                canvas.itemconfig(obj, fill=color)
                color_label = 'color' if 'line' in canvas.obj_tag else 'bgcolor'
                canvas.obj_storage[canvas.obj_tag][color_label].append(color)
            canvas.obj_storage[canvas.obj_tag]['modifications'].append('fill')
        elif canvas.hover:
            canvas['background'] = color

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
            canvas.modified_objs.append(canvas.obj_tag)
            if 'brush' in canvas.obj_tag:
                for member in canvas.find_withtag(canvas.obj_tag):
                    canvas.itemconfig(member, width=thickness)
                    canvas.obj_storage[canvas.obj_tag]['size'].append(thickness)
            else:
                obj = canvas.find_withtag(canvas.obj_tag)
                canvas.itemconfig(obj, width=thickness)
                canvas.obj_storage[canvas.obj_tag]['thickness'].append(thickness)
            canvas.obj_storage[canvas.obj_tag]['modifications'].append('thickness')

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

        if canvas.obj_tag and 'brush' not in canvas.obj_tag and 'line' not in canvas.obj_tag:
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

            if storage[last_modified_obj]['modifications'][-1] == 'fill':
                if 'brush' in last_modified_obj:
                    for member in canvas.find_withtag(last_modified_obj):
                        canvas.itemconfig(member, fill=storage[last_modified_obj]['color'][-2])
                    del storage[last_modified_obj]['color'][-1]
                else:
                    obj = canvas.find_withtag(last_modified_obj)
                    color = 'color' if 'line' in last_modified_obj else 'bgcolor'
                    canvas.itemconfig(obj, fill=storage[last_modified_obj][color][-2])
                    del storage[last_modified_obj][color][-1]
                del storage[last_modified_obj]['modifications'][-1]
            elif storage[last_modified_obj]['modifications'][-1] == 'creation':
                canvas.delete(last_modified_obj)
                del storage[last_modified_obj]
            elif storage[last_modified_obj]['modifications'][-1] == 'move':
                if 'brush'in last_modified_obj:
                    x1, y1 = storage[last_modified_obj]['coords'][-1][-2:]
                    x2, y2 = storage[last_modified_obj]['coords'][-2][-2:]
                    canvas.move(last_modified_obj, x2-x1, y2-y1)
                else:
                    canvas.coords(last_modified_obj, *storage[last_modified_obj]['coords'][-2])
                del storage[last_modified_obj]['coords'][-1]
                del storage[last_modified_obj]['modifications'][-1]

            elif storage[last_modified_obj]['modifications'][-1] == 'thickness':
                if 'brush' in last_modified_obj:
                    for member in canvas.find_withtag(last_modified_obj):
                        canvas.itemconfig(member, width=storage[last_modified_obj]['size'][-2])
                    del storage[last_modified_obj]['size'][-1]
                else:
                    obj = canvas.find_withtag(last_modified_obj)
                    canvas.itemconfig(obj, width=storage[last_modified_obj]['thickness'][-2])
                    del storage[last_modified_obj]['thickness'][-2]
                del storage[last_modified_obj]['modifications'][-1]
            elif storage[last_modified_obj]['modifications'][-1] == 'outcolor':
                obj = canvas.find_withtag(last_modified_obj)
                canvas.itemconfig(obj, outline=storage[last_modified_obj]['outcolor'][-2])
                del storage[last_modified_obj]['outcolor'][-1]
                del storage[last_modified_obj]['modifications'][-1]

            del canvas.modified_objs[-1]