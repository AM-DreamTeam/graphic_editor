# Импортированные модули
from graphic_lib import _graphic_core as gcore
from tkinter import *
from PIL import Image, ImageTk


class App:
    """ App - пример приложение для проверки модуля """

    def __init__(self, root):
        ico = Image.open('images/visualist.png')
        ico.thumbnail((64, 64), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(ico)

        root.title('Visualist')
        root.wm_iconphoto(False, photo)

        frame_main = Frame(root)
        frame_main.pack()

        canvas = gcore.CustomCanvas(frame_main, width=gcore.DEFAULT_CANVAS_W, height=gcore.DEFAULT_CANVAS_H, bg=gcore.DEFAULT_CANVAS_BG)
        canvas.pack(side=RIGHT)

        events = gcore.Events(root, gcore.DEFAULT_USED_EVENTS, canvas)

        btnClear = Button(frame_main, text='*отчистить*', command=events.event_btnClear)
        btnClear.pack(side=TOP, pady=5)

        btnMove = Button(frame_main, text='*подвинуть*',
                         command=lambda ms=gcore.DEFAULT_MOUSE_SPEED:
                         events.event_move(mouse_speed=ms))
        btnMove.pack(side=TOP, pady=5)

        btnEraser = Button(frame_main, text='*ластик*',
                           command=lambda s=gcore.DEFAULT_ERASER_SIZE:
                           events.event_btnEraser(size=s))
        btnEraser.pack(side=TOP, pady=5)

        btnBrush = Button(frame_main, text='*кисть*',
                          command=lambda s=gcore.DEFAULT_BRUSH_SIZE, clr=gcore.DEFAULT_FIRST_COLOR:
                          events.event_btnBrush(size=s, color=clr))
        btnBrush.pack(side=TOP, pady=5)

        btnCreateLine = Button(frame_main, text='*линия*',
                               command=lambda t=gcore.DEFAULT_THICKNESS, clr=gcore.DEFAULT_FIRST_COLOR:
                               events.event_btnCreateLine(thickness=t, color=clr))
        btnCreateLine.pack(side=TOP, pady=5)

        btnCreateOval = Button(frame_main, text='*эллипс*',
                               command=lambda t=gcore.DEFAULT_THICKNESS, outclr=gcore.DEFAULT_FIRST_COLOR,
                                              bgclr=gcore.DEFAULT_SECOND_COLOR:
                               events.event_btnCreateOval(thickness=t, bgcolor=bgclr, outcolor=outclr))
        btnCreateOval.pack(side=TOP, pady=5)

        btnCreateRectangle = Button(frame_main, text='*прямоугольник*',
                                    command=lambda t=gcore.DEFAULT_THICKNESS, outclr=gcore.DEFAULT_FIRST_COLOR,
                                                   bgclr=gcore.DEFAULT_SECOND_COLOR:
                                    events.event_btnCreateRectangle(thickness=t, bgcolor=bgclr, outcolor=outclr))
        btnCreateRectangle.pack(side=TOP, pady=5)

        root.bind('<Control-x>', quit)
        root.bind('<Control-z>', lambda event: events.event_undo())
        root.bind('<Control-s>', lambda event: print(canvas.obj_storage))


root = Tk(className='Visualist')
App(root)
root.mainloop()