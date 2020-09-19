# Импортированные модули
from tkinter import *


# Глобальные переменные
old_point = None
used_events = ['<B1-Motion>', '<ButtonPress-1>', '<ButtonRelease-1>']

root = Tk()
root.title('Graphic Basic')

frame_main = Frame(root)


# Базовые функции
def unbind_all_events(used_events: list) -> None:
    ''' Очищает все действующие бинды

        Аргументы:
            used_events: list - список из всех задействованных событий

        Глобальные перменные:
            root: tkinter.Tk - приложение

        Возвращает:
            None

        Побочный эффект:
            Очищает все бинды - used_events
    '''

    global root

    for _ in used_events:
        root.unbind(_)


# Функции для отрисовки графики
def draw_points(event: Event, canvas: Canvas, thickness: int = 5) -> None:
    ''' Рисует точку на месте курсора

        Аргументы:
            event: tkinter.Event - событие, по которому считываем положение курсора
            canvas: tkinter.Canvas - canvas (слой), на котором рисуем точку
            thickness: int - жирность точки (овала)

        Возвращает:
            None

        Побочный эффект:
            Отрисовка точки (овала) на canvas'e (слое)
    '''

    x1, y1 = event.x - 1, event.y - 1
    x2, y2 = event.x + 1, event.y + 1

    canvas.create_oval(x1, y1, x2, y2, fill = 'black', width = thickness)


def draw_line(event: Event, canvas: Canvas, thickness: int = 2) -> None:
    ''' Рисует линию по заданным точкам

        Аргументы:
            event: tkinter.Event - событие, по которому считывается положение курсора
            canvas: tkinter.Canvas - canvas (слой), на котором рисуем прямую
            thickness: int - жирность линии (отрезка)

        Глобальные перменные:
            old_point: tuple - старые координаты точки, которая является началом линии (отрезка)

        Возвращает:
            None

        Побочный эффект:
            Отрисовка линии по заданным точкам на canvas'e
    '''

    global old_point

    if str(event.type) == 'ButtonPress':
        old_point = event.x, event.y
        draw_points(event, canvas, thickness + 1)
    elif str(event.type) == 'ButtonRelease':
        x1, y1 = event.x, event.y
        x2, y2 = old_point
        canvas.create_line(x1, y1, x2, y2, width = thickness)
        draw_points(event, canvas, thickness + 1)


# Функции (события) для кнопок
def btn_clear_Event(used_events: list, canvas: Canvas) -> None:
    ''' Событие для кнопки btnClear

        Аргументы:
            used_events - список из всех задействованных событий
            canvas: tkinter.Canvas - canvas (слой), который очищается

        Возвращает:
            None

        Побочный эффект:
            Очистка canvas'a (слоя)
    '''

    unbind_all_events(used_events)
    canvas.delete('all')


def btn_brush_Event(used_events: list, canvas: Canvas, thickness: int = 5) -> None:
    ''' Событие для кнопки btnBrush

        Аргументы:
            used_events - список из всех задействованных событий
            canvas: tkinter.Canvas - canvas (слой), на котором будет отрисовываться последовательность точек (овалов)
            thickness: int - жирность точки (овала)

        Глобальные переменные:
            root: tkinter.Tk - приложение

        Возвращает:
            None

        Побочный эффект:
            Очищаются все бинды и создаётся новый бинд на <B1-Motion> - отрисовка последовательности точек (овалов)
    '''

    global root

    unbind_all_events(used_events)

    root.bind('<B1-Motion>', lambda event, c = canvas, t = thickness: draw_points(event, canvas, t))


def btn_createLine_Event(used_events: list, canvas: Canvas, thickness: int = 2) -> None:
    ''' Событие для кнопки btnCreateLine

        Аргументы:
            used_events - список из всех задействованных событий
            canvas: tkinter.Canvas - canvas (слой), на котором будет отрисовываться линия (отрезок)
            thickness: int - жирность линии

        Глобальная перменная:
            root: tkinter.Tk - приложение

        Возвращает:
            None

        Побочный эффект:
            Очищает все бинды и создаёт 2 новых бинла <ButtonPress-1>, <ButtonRelease-1> - отрисовка линии (отрезка)
    '''

    global root

    unbind_all_events(used_events)

    root.bind('<ButtonPress-1>', lambda event, c = canvas, t = thickness: draw_line(event, c, t))
    root.bind('<ButtonRelease-1>', lambda event, c = canvas, t = thickness: draw_line(event, c, t))


# Работа с графическим интерфейсом и упаковками
frame_main.pack()

canvas = Canvas(frame_main, width = 800, height = 600, bg = 'white')
canvas.pack(side = RIGHT)

btnClear = Button(frame_main, text = '*отчистить*', command = lambda ue = used_events, c = canvas:  btn_clear_Event(ue, c))
btnClear.pack(side = TOP, pady = 5)

btnBrush = Button(frame_main, text = '*кисть*', command = lambda ue = used_events, c = canvas, t = 5: btn_brush_Event(ue, c, t))
btnBrush.pack(side = TOP, pady = 5)

btnCreateLine = Button(frame_main, text = '*линия*', command = lambda ue = used_events, c = canvas, t = 2: btn_createLine_Event(ue, c, t))
btnCreateLine.pack(side = TOP, pady = 5)

root.bind('<Control-x>', quit)

root.mainloop()
