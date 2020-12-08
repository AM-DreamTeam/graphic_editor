# Импортированные модули
from tkinter import *
import tkinter.font as tkFont
import tkinter.colorchooser
from tkinter.ttk import Combobox
from tkinter.messagebox import showerror


class TextSettingsWindow(Toplevel):
    """ TextSettingsWindow - модальное окно для настроек текста

        Аргументы:
            * root: tkinter.Tk - главное окно
            ** text: str - текст, который будет напечатан
            ** family: str - семейство шрифта для текста
            ** size: str - размер текста
            ** italic: bool - нужно ли делать текст курсивом
            ** bold: bool - нужно ли делать текст жирным
            ** color: str - цвет текста

        Методы:
            * choose_color(self) -> None
            * submit(self) -> None
            * get_data(self) -> tuple
    """

    def __init__(self, root, *, text, family, size, italic, bold, color, **kwargs):
        super().__init__(**kwargs)

        self._selected_color = color

        self.wm_title('Текст')

        # Frame с текстом

        __frame_text = Frame(self)

        __lblText = Label(__frame_text, text='Введите текст: ')
        __lblText.grid(row=0, column=0)

        __frame_scroll = Frame(__frame_text)

        self._textBox = Text(__frame_scroll, width=20, height=5, wrap=WORD)
        self._textBox.insert(1.0, text)

        __scrollText = Scrollbar(__frame_scroll, command=self._textBox.yview)
        __scrollText.pack(side=RIGHT, fill=Y)

        self._textBox.config(yscrollcommand=__scrollText.set)
        self._textBox.pack(side=LEFT)

        self._text = self._textBox.get('1.0', END)

        __frame_scroll.grid(row=0, column=1)
        __frame_text.pack(side=TOP, padx=5, pady=5)

        # Frame с настройками

        __frame_options = LabelFrame(self, text='Параметры текста')

        __lblColor = Label(__frame_options, text='Цвет: ')
        __lblColor.grid(row=0, column=0)

        self._btnColor = Button(__frame_options, bg=self._selected_color, activebackground=self._selected_color, command=self.choose_color)
        self._btnColor.grid(row=0, column=1, sticky=W)

        __lblFont = Label(__frame_options, text='Шрифт: ')
        __lblFont.grid(row=1, column=0)

        __tkFonts = sorted(list(tkFont.families()))

        self._var_family = StringVar(__frame_options)
        self._var_family.set(family)
        __box_families = Combobox(__frame_options,
                                  textvariable=self._var_family,
                                  values=__tkFonts,
                                  width=24)
        __box_families.grid(row=1, column=1, sticky=W)

        __lblSize = Label(__frame_options, text='Размер: ')
        __lblSize.grid(row=2, column=0)

        self._var_size = StringVar(__frame_options)
        self._var_size.set(size)
        __entrySize = Entry(__frame_options,
                            textvariable=self._var_size,
                            width=4)
        __entrySize.grid(row=2, column=1, sticky=W)

        __lblStyle = Label(__frame_options, text='Стиль: ')
        __lblStyle.grid(row=3, column=0)

        __frame_styles = Frame(__frame_options)
        self._var_italic = BooleanVar(__frame_styles)
        self._var_italic.set(italic)
        __checkItalic = Checkbutton(__frame_styles,
                                    text='курсив',
                                    variable=self._var_italic,
                                    onvalue=1, offvalue=0)
        __checkItalic.pack(side=LEFT, padx=5, pady=5)

        self._var_bold = BooleanVar(__frame_styles)
        self._var_bold.set(bold)
        __checkBold = Checkbutton(__frame_styles,
                                  text='жирный',
                                  variable=self._var_bold,
                                  onvalue=1, offvalue=0)
        __checkBold.pack(side=LEFT, padx=5, pady=5)

        __frame_styles.grid(row=3, column=1)

        __frame_options.pack(side=TOP, padx=5, pady=5)

        btnSubmit = Button(self, text='Применить', command=self.submit)
        btnSubmit.pack(side=RIGHT, padx=5, pady=5)

        self.transient(root)
        self.wait_visibility()
        self.grab_set()
        self.focus_set()

    def choose_color(self):
        """ Событие для кнопки self._btnColor

            Возвращает:
                None

            Побочный эффект:
                Подгружает модальное окно с выбором цвета и перезаписывает переменную хранения текста + меняет цвет кнопки
        """

        self._selected_color = tkinter.colorchooser.askcolor(title='Цвета', parent=self)[1]
        self._btnColor.config(bg=self._selected_color, activebackground=self._selected_color)

    def submit(self):
        """ Событие для кнопки btnSubmit

            Возвращает:
                None

            Побочный эффект:
                Закрывает текущее модальное окно, если всё подходит под условие выхода
        """

        self._text = self._textBox.get("1.0", END).rstrip()
        if self._text != '' and self._var_size.get().isnumeric() and self._var_family.get() in tkFont.families():
            self.destroy()
        else:
            showerror(title='Ошибка', message='Введённые данные некорректны')

    def get_data(self):
        """ Возращает выбранные данные из модального окна

            Возвращает:
                tuple - настройки текста из модального окна
        """

        self.wait_window()
        data = (self._text.rstrip(), self._selected_color, self._var_family.get(), self._var_size.get(), self._var_italic.get(), self._var_bold.get())
        return data
