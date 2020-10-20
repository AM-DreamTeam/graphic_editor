# Импортированные модули
from tkinter import *
from _custom_objects import CustomCanvas
from typing import List


# Глобальные переменные
_USED_EVENTS = ('<B1-Motion>', '<ButtonPress-1>','<ButtonRelease-1>')
root = Tk()


class Basic:
    """ Basic - базовые функции

        Статические методы:
            * unbind_all_events(used_events: List[str])
    """

    @staticmethod
    def unbind_all_events(used_events: List[str]) -> None:
        """ Очищает все действующие бинды

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды - used_events
        """

        for _ in used_events:
            root.unbind(_)


class Draw:
    """ Draw - отрисовка элементов

        Статические методы:
            * draw_points(event: Event, canvas: Canvas, *, size: int = 5, color: str = 'black')
            * draw_oval(event: Event, canvas: Canvas, thickness: int = 2, )
            * draw_line(event: Event, canvas, Canvas, thickness: int = 2)
    """

    @staticmethod
    def point(event: Event, canvas: Canvas,
               *,
               size: int = 5,
               color: str = 'black') -> None:
        """ Рисует точку на месте курсора

            Аргументы:
                * event: tkinter.Event - событие, по которому считываем положение курсора
                * canvas: tkinter.Canvas - canvas (слой), на котором рисуем точку
                ** size: int - размер точки (овала)
                ** color: str - цвет точки (овала)

            Возвращает:
                None

            Побочный эффект:
                Отрисовка точки (овала) на canvas'e (слое)
        """

        x1, y1 = event.x - 1, event.y - 1
        x2, y2 = event.x + 1, event.y + 1

        canvas.create_oval(x1, y1, x2, y2, fill=color, width=size)


    # TODO: добавить параметр dash
    @staticmethod
    def line(event: Event, canvas: Canvas,
             *,
             thickness: int = 2,
             color: str = 'black') -> None:
        """ Рисует линию по заданным точкам

             Аргументы:
                * event: tkinter.Event - событие, по которому считывается положение курсора
                * canvas: tkinter.Canvas - canvas (слой), на котором рисуем прямую
                ** thickness: int - жирность линии (отрезка)
                ** color: str - цвет линии (отрезка)

            Возвращает:
                None

            Побочный эффект:
                Отрисовка линии по заданным точкам на canvas'e
        """

        if str(event.type) == 'ButtonPress':
            canvas.old_point = event.x, event.y
        elif str(event.type) == 'ButtonRelease':
            x1, y1 = event.x, event.y
            x2, y2 = canvas.old_point
            canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color)
        elif str(event.type) == 'Motion':
            x1, y1 = event.x, event.y
            x2, y2 = canvas.old_point
            l = canvas.create_line(x1, y1, x2, y2, width=thickness, fill=color)

            if canvas.obj_lines:
                canvas.delete(canvas.obj_lines[-1])
                canvas.obj_lines = canvas.obj_lines[:-1]

            canvas.obj_lines.append(l)


    # TODO: добавить параметр dash
    @staticmethod
    def oval(event: Event, canvas: Canvas,
             *,
             thickness: int = 2,
             bgcolor: str = None,
             outcolor: str = 'black') -> None:
        """ Рисует окружность по заданным точкам

            Аргументы:
                * event: tkinter.Event - событие, по которому считавается положение курсора
                * canvas: tkinter.Canvas - canvas (слой), на котором рисуем окружность
                ** thickness: int - жирность обводки окружности
                ** bgcolor: str - цвет заливки окружности
                ** outcolor: str - цвет обводки окружности

            Возвращает:
                None

            Побочный эффект:
                Отрисовка окружность по заданным точкам на canvas'е
        """

        if str(event.type) == 'ButtonPress':
            canvas.old_point = event.x, event.y
        elif str(event.type) == 'ButtonRelease':
            x1, y1 = event.x, event.y
            x2, y2 = canvas.old_point
            canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)
        elif str(event.type) == 'Motion':
            x1, y1 = event.x, event.y
            x2, y2 = canvas.old_point
            o = canvas.create_oval(x1, y1, x2, y2, width=thickness, fill=bgcolor, outline=outcolor)

            if canvas.obj_ovals:
                canvas.delete(canvas.obj_ovals[-1])
                canvas.obj_ovals = canvas.obj_ovals[:-1]

            canvas.obj_ovals.append(o)


class Events:
    """ Events - содержит все события

        Статические методы класса:
            * event_btnClear(used_events: List[str], canvas: Canvas)
            * event_btnBrush_Event(used_events: List[str], canvas: Canvas, thickness: int = 5)
            * event_btnCreateLine(used_events: List[str], canvas: Canvas, thickness: int = 2)
            * event_btnCreateOval(used_events: List[str], canvas: Canvas, thickness: int = 2)
    """

    @staticmethod
    def event_btnClear(used_events: List[str], canvas: Canvas) -> None:
        """ Событие для кнопки btnClear

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий
                * canvas: tkinter.Canvas - canvas (слой), который очищается

            Возвращает:
                None

            Побочный эффект:
                Очистка canvas'a (слоя)
        """

        Basic.unbind_all_events(used_events)
        canvas.delete('all')


    @staticmethod
    def event_btnBrush(used_events: List[str], canvas: Canvas,
                  *,
                  size: int = 5,
                  color: str = 'black') -> None:
        """ Событие для кнопки btnBrush

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий
                * canvas: tkinter.Canvas - canvas (слой), на котором будет отрисовываться последовательность точек (овалов)
                ** size: int - размер точки (овала)
                ** color: str - цвет точки (овала)

            Возвращает:
                None

            Побочный эффект:
                Очищаются все бинды и создаётся новый бинд на <B1-Motion> - отрисовка последовательности точек (овалов)
        """

        Basic.unbind_all_events(used_events)

        root.bind('<B1-Motion>', lambda event, c=canvas, s=size, clr=color: Draw.point(event, canvas,
                                                                                        size=s,
                                                                                        color=clr))


    @staticmethod
    def event_btnCreateLine(used_events: List[str], canvas: Canvas,
                            *,
                           thickness: int = 2,
                           color: str = 'black') -> None:
        """ Событие для кнопки btnCreateLine

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий
                * canvas: tkinter.Canvas - canvas (слой), на котором будет отрисовываться линия (отрезок)
                ** thickness: int - жирность линии
                ** color: str - цвет линии

            Возвращает:
                None

            Побочный эффект:
                Очищает все бинды и создаёт 2 новых бинла <ButtonPress-1>, <ButtonRelease-1> - отрисовка линии (отрезка)
        """

        Basic.unbind_all_events(used_events)

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>'):
            root.bind(event, lambda event, c=canvas, t=thickness, clr=color: Draw.line(event, c,
                                                                                       thickness=t,
                                                                                       color=clr))


    @staticmethod
    def event_btnCreateOval(used_events: List[str], canvas: Canvas,
                            *,
                            thickness: int = 2,
                            bgcolor: str = None,
                            outcolor: str = 'black') -> None:
        """ Событие для кнопки btnCreateOval

            Аргументы:
                * used_events: List[str] - список из всех задействованных событий
                * canvas: tkinter.Canvas - canvas (слой), на котором рисуем окружность
                ** thickness: int - жирность обводки окружности
                ** bgcolor: str - цвет заливки овала
                ** outcolor: str - цвет обводки овала

            Возвращает:
                None

            Побочный эффект:
                Очищаются все бинды и создаётся новый бинд на <B1-Motion> - отрисовка последовательности точек (овалов)
        """

        Basic.unbind_all_events(used_events)

        for event in ('<ButtonPress-1>', '<ButtonRelease-1>', '<B1-Motion>'):
            root.bind(event, lambda event, c=canvas, t=thickness, bgclr=bgcolor, outclr=outcolor: Draw.oval(event, c,
                                                                                                    thickness=t,
                                                                                                    bgcolor=bgclr,
                                                                                                    outcolor=outclr))


# Создаём пример приложения
if __name__ == '__main__':

    class App:
        """ App - тестовое приложение для проверки функций """

        def __init__(self, _USED_EVENTS):
            root.title('Graphic Basic')

            frame_main = Frame(root)
            frame_main.pack()

            canvas = CustomCanvas(frame_main, width=800, height=600, bg='white')
            canvas.pack(side=RIGHT)

            btnClear = Button(frame_main, text='*отчистить*',
                              command=lambda ue=_USED_EVENTS, c=canvas: Events.event_btnClear(ue, c))
            btnClear.pack(side=TOP, pady=5)

            btnBrush = Button(frame_main, text='*кисть*',
                              command=lambda ue=_USED_EVENTS, c=canvas, s=5, clr='black':
                              Events.event_btnBrush(ue, c, size=s, color='black'))
            btnBrush.pack(side=TOP, pady=5)

            btnCreateLine = Button(frame_main, text='*линия*',
                                   command=lambda ue=_USED_EVENTS, c=canvas, t=2, clr='black':
                                   Events.event_btnCreateLine(ue, c, thickness=t, color=clr))
            btnCreateLine.pack(side=TOP, pady=5)

            btnCreateOval = Button(frame_main, text='*овал*',
                                   command=lambda ue=_USED_EVENTS, c=canvas, t=2, bgclr=None, outclr='black':
                                   Events.event_btnCreateOval(ue, c, thickness=t, bgcolor=bgclr, outcolor=outclr))
            btnCreateOval.pack(side=TOP, pady=5)

            root.bind('<Control-x>', quit)


    App(_USED_EVENTS)
    root.mainloop()