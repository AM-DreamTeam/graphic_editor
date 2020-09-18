# Импортированные модули
from tkinter import *

# Глобальные переменные
activeBrush = False
activeCreateLine = False

root = Tk()
root.title('Graphic Basic')

frame_main = Frame(root)


# Функции для отрисовки графики
def draw_points(event: Event, canvas: Canvas, brush_size: int = 5) -> None:
    ''' Рисует точку на месте курсора

        Аргументы:
                event: tkinter.Event - событие, по которому считываем положение курсора
                canvas: tkinter.Canvas - canvas (слой), на котором рисуем точку
                brush_size: int - жирность точки

        Возвращает:
                None

        Побочный эффект:
                Отрисовка точки (овала) на canvas (слой)

    '''

    x1, y1 = event.x - 1, event.y - 1
    x2, y2 = event.x + 1, event.y + 1

    canvas.create_oval(x1, y1, x2, y2, fill = 'black', width = brush_size)


def draw_line(event: Event, canvas: Canvas) -> None:
    canvas.create_line(0, 0, event.x, event.y)

# Функции (события) для кнопок
def btn_clear_Event(canvas: Canvas) -> None:
    ''' Событие для кнопки btnClear

        Аргументы:
            canvas: tkinter.Canvas - canvas (слой), который очищается

        Возвращает:
            None

        Побочный эффект:
            Очистка canvas'a (слоя)

    '''

    canvas.delete('all')


def btn_brush_Event(event: Event, canvas: Canvas, brush_size: int) -> None:
    ''' Событие для кнопки btnBrush

        Аргументы:
            event: tkinter.Event - событие, по которому будет вызываться отрисовка точек (овалов)
            canvas: tkinter.Canvas - canvas (слой), на котором будут отрисовываться
            brush_size: int - жирность точки (овала)

        Глобальные переменные:
            activeBrush: bool - включает или отключает кисть
            root: tkinter.Tk - приложение

        Возвращает:
            None

        Побочный эффект:
            activeBrush: True - на событие event биндиться функция draw_points
            activeBrush: False - анбиндит событие
    '''

    global activeBrush, root

    if activeBrush == False:
        root.bind(event, lambda e, c = canvas, bs = brush_size: draw_points(e, canvas, bs))
        activeBrush = True
    else:
        root.unbind(event)
        activeBrush = False


def btn_createLine_Event(event: Event, canvas: Canvas) -> None:

    global activeCreateLine, root

    if activeCreateLine == False:
        root.bind(event, lambda e = event, c = canvas: draw_line(e, c))
        activeCreateLine = True
    else:
        root.unbind(event)
        activeCreateLine = False


# Работа с графическим интерфейсом и упаковкам
frame_main.pack()

canvas = Canvas(frame_main, width = 800, height = 600, bg = 'white')
canvas.pack(side = RIGHT)

btnClear = Button(frame_main, text = '*отчистить*', command = lambda c = canvas:  btn_clear_Event(c))
btnClear.pack(side = TOP, pady = 5)

btnBrush = Button(frame_main, text = '*кисть*', command = lambda e = '<B1-Motion>', c = canvas, bs = 2: btn_brush_Event(e, c, bs))
btnBrush.pack(side = TOP, pady = 5)

btnCreateLine = Button(frame_main, text = '*линия*', command = lambda e = '<Button-1>', c = canvas: btn_createLine_Event(e, c))
btnCreateLine.pack(side = TOP, pady = 5)

root.bind('<Control-x>', quit)

root.mainloop()
