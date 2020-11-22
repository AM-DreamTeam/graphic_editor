# Импротированные модули
from ._basic import *
from tkinter import TRUE, ROUND
from math import atan2, sin, cos, floor


class Draw:
    """ Draw - логика работы с графическими примитивами

        Аргументы:
            * event: tkinter.Event - событие, по которому считывается положение курсора
            * canvas: _custom_objects.CustomCanvas - canvas (слой), на котором происходит отрисовка

        Методы:
            * point(*, size: int = DEFAULT_SIZE, color: str = DEFAULT_FIRST_COLOR, eraser: bool = False, debug_mode: bool = False) -> None
            * oval(*, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * line(*, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * polygon(self, *, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * rectangle(*, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None
            * move(*, mouse_speed: int = DEFAULT_MOUSE_SPEED) -> None
            * fill_objects(self, *, color: str = DEFAULT_CHANGE_COLOR) -> None
            * quick_eraser(self) -> None
            * on_canvas(self) -> None
    """

    def __init__(self, event, canvas):
        self._event = event
        self._canvas = canvas

    def point(self,
              *,
              size,
              color,
              eraser = False,
              debug_mode = False):
        """ Рисует точку на месте курсора

            Аргументы:
                ** size: int - размер точки (отрезок)
                ** color: str - цвет точки (отрезок)
                ** eraser: bool - режим работы с ластиком
                ** debug_mode: bool - режим отладчика

            Возвращает:
                None

            Побочный эффект:
                Отрисовка точки (отрезок) на canvas'e (слое)
        """

        event, canvas = self._event, self._canvas

        x1, y1 = event.x, event.y

        if str(event.type) == 'ButtonRelease' and canvas.line_sequences and canvas.hover:
            canvas.old_point = None
            if not eraser:
                tag = f'brush{len(canvas.obj_storage) + 1}'
                x_min, y_min, x_max, y_max = transform_line_sequence(canvas.line_sequences)
                canvas.obj_storage[tag] = (x_min, y_min, x_max, y_max)
                if debug_mode:
                    canvas.create_rectangle(x_min, y_min, x_max, y_max, dash=(5, 3), tags=tag)
                canvas.addtag_overlapping(tag, x_min, y_min, x_max, y_max)
                canvas.line_sequences = []
        elif str(event.type) == 'Motion':
            if canvas.old_point:
                x2, y2 = canvas.old_point
                canvas.create_line(x1, y1, x2, y2, width=size, fill=color, smooth=TRUE, capstyle=ROUND)
                if not eraser:
                    canvas.line_sequences.append([(x1, y1), (x2, y2)])
            canvas.old_point = x1, y1

    def line(self,
             *,
             thickness,
             color):
        """ Рисует линию по заданным точкам

             Аргументы:
                ** thickness: int - жирность линии (отрезка)
                ** color: str - цвет линии (отрезка)

            Возвращает:
                None

            Побочный эффект:
                Отрисовка линии по заданным точкам на canvas'e
        """

        event, canvas = self._event, self._canvas

        new_point = event.x, event.y

        if str(event.type) == 'ButtonPress' and canvas.hover:
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point and canvas.hover:
            tag = f'line{len(canvas.obj_storage) + 1}'
            x2, y2 = canvas.old_point
            x1, y1 = transform_line_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color, smooth=TRUE, capstyle=ROUND, tags=tag)
            canvas.obj_storage[tag] = (x1, y1, x2, y2)
            canvas.delete(canvas.obj_line)
        elif str(event.type) == 'Motion' and canvas.old_point:
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
                ** thickness: int - жирность обводки эллипса
                ** bgcolor: str - цвет заливки эллипса
                ** outcolor: str - цвет обводки эллипса

            Возвращает:
                None

            Побочный эффект:
                Отрисовка эллипса по заданным точкам на canvas'е
        """

        event, canvas = self._event, self._canvas

        new_point = event.x, event.y

        if str(event.type) == 'ButtonPress' and canvas.hover:
            canvas.old_point = event.x, event.y
        elif str(event.type) == 'ButtonRelease' and canvas.old_point and canvas.hover:
            tag = f'oval{len(canvas.obj_storage) + 1}'
            x1, y1 = transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor, tags=tag)
            canvas.obj_storage[tag] = (x1, y1, x2, y2)
            canvas.delete(canvas.obj_oval)
        elif str(event.type) == 'Motion' and canvas.old_point:
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
                ** thickness: int - жирность обводки прямоугольник
                ** bgcolor: str - цвет заливки прямоугольник
                ** outcolor: str - цвет обводки прямоугольник

            Возвращает:
                None

            Побочный эффект:
                Отрисовка прямоугольника по заданным точкам на canvas'е
        """

        event, canvas = self._event, self._canvas

        new_point = event.x, event.y

        if str(event.type) == 'ButtonPress' and canvas.hover:
            canvas.old_point = new_point
        elif str(event.type) == 'ButtonRelease' and canvas.old_point and canvas.hover:
            tag = f'rectangle{len(canvas.obj_storage)+1}'
            x1, y1 = transform_coords(canvas.old_point, new_point) if 'Control' in str(event) else new_point
            x2, y2 = canvas.old_point
            canvas.create_rectangle(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor, tags=tag)
            canvas.obj_storage[tag] = (x1, y1, x2, y2)
            canvas.delete(canvas.obj_rectangle)
        elif str(event.type) == 'Motion' and canvas.old_point:
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
                ** thickness: int - жирность обводки многоугольника
                ** bgcolor: str - цвет заливки многоугольника
                ** outcolor: str - цвет обводки многоугольника

            Возвращает:
                None

            Побочный эффект:
                Отрисовка многоугольника по заданным точкам на canvas'e
        """

        event, canvas = self._event, self._canvas

        new_point = event.x, event.y

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
                polygon = canvas.create_polygon(*flatten(canvas.line_sequences), fill=bgcolor, outline=outcolor, tags=tag)
                canvas.line_sequences = []
                x_min, y_min, x_max, y_max = transform_line_sequence(partition_coords(canvas.coords(polygon), 4, 2))
                canvas.obj_storage[tag] = (x_min, y_min, x_max, y_max)
                canvas.delete('temp_line')
            else:
                canvas.line_sequences.append([(x2, y2), (x1, y1)])
                canvas.old_point = x1, y1
        elif str(event.type) == 'Motion' and canvas.old_point:
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

        if str(event.type) == 'ButtonPress':
            canvas.obj_tag = detect_object(event, canvas)
        elif str(event.type) == 'ButtonRelease' and canvas.obj_tag:
            if 'brush' in canvas.obj_tag:
                raw_points = [tuple(map(lambda x: floor(x), canvas.coords(obj))) for obj in canvas.find_withtag(canvas.obj_tag)]
                points_storage = list(map(lambda sublist: [sublist[i:i+2] for i in range(0, len(sublist), 2)], raw_points))
                x_min, y_min, x_max, y_max = transform_line_sequence(points_storage)
                canvas.obj_storage[canvas.obj_tag] = (x_min, y_min, x_max, y_max)
            else:
                canvas.obj_storage[canvas.obj_tag] = canvas.coords(canvas.obj_tag)
            canvas.obj_tag = None
        elif str(event.type) == 'Motion' and canvas.obj_tag:
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
                ** color: str - цвет в который будет перекрашен объект

            Возвращает:
                None

            Побочный эффект:
                Перекрашивает объект в цвет color на canvas'e (слое)
        """

        event, canvas = self._event, self._canvas
        canvas.obj_tag = detect_object(event, canvas)

        if canvas.obj_tag:
            if 'brush' in canvas.obj_tag:
                for member in canvas.find_withtag(canvas.obj_tag):
                    canvas.itemconfig(member, fill=color)
            else:
                obj = canvas.find_withtag(canvas.obj_tag)
                canvas.itemconfig(obj, fill=color)
        elif canvas.hover:
            canvas['background'] = color

    def quick_eraser(self):
        """ 'Быстрый' ластик

            Возвращает:
                None

            Побочный эффект:
                За одно касание удаляет графический примитив
        """

        event, canvas = self._event, self._canvas

        canvas.obj_tag = detect_object(event, canvas)
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