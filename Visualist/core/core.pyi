""" Type hintings """


from tkinter import Event, Canvas, Tk, StringVar, Toplevel, Scale
from tkinter.ttk import Notebook
from tkinter.font import Font
from typing import (
    Callable,
    Tuple,
    Iterable
)


# _defaults.py
" ~ graphic_lib ~ "
DEFAULT_USED_EVENTS: Tuple[str]
DEFAULT_FIRST_COLOR: str
DEFAULT_SECOND_COLOR: str
DEFAULT_CHANGE_COLOR: str
DEFAULT_THICKNESS: int
DEFAULT_BRUSH_SIZE: int
DEFAULT_ERASER_SIZE: int
DEFAULT_MOUSE_SPEED: int
DEFAULT_CANVAS_W: int
DEFAULT_CANVAS_H: int
DEFAULT_CANVAS_BG: str
" ~ image_lib ~"
DEFAULT_FILTERS_1: Iterable[str]
DEFAULT_FILTERS_2: Iterable[str]
DEFAULT_FILTERS_3: Iterable[str]


# _custom_objects.py
class CustomCanvas(Canvas):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        " ~ graphic_lib ~ "
        self.old_point: (None, Tuple[int, int])
        self.obj_oval: (None, int)
        self.obj_line: (None, int)
        self.obj_rectangle: (None, int)
        self.obj_horizontal_axis = (None, int)
        self.obj_vertical_axis = (None, int)
        self.line_sequences: list
        self.obj_storage: dict
        self.modified_objs: list
        self.start_point: (None, Tuple[int, int])
        self.obj_tag: (None, str)
        self.hover: bool
        " ~ image_lib ~ "
        self.img: dict
        self.undo: list
        ...

class NotebookTabs(Notebook):
    __initialized = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active = int
        self._closed_tabs = []
        ...

    def on_close_press(self, event: Event) -> None: ...
    def on_close_release(self, event: Event) -> None: ...
    def reestablish_tab(self) -> None: ...
    def __initialize_custom_style(self) -> None: ...


class CustomNotebook(NotebookTabs):
    image_processing = None
    events = None
    def __init__(self, root: Tk, **kwargs) -> None:
        super().__init__(**kwargs)
        self._count: int
        self.root: Tk
        self.image_processing: Img
        self.events: Events
        self._canvases: list
        ...

    def create_new_canvas(self) -> None: ...
    def select_curr_tab(self, event: Event) -> None: ...
    def undo(self, event: Event) -> None: ...


""" ============= graphic_lib ============ """


# graphic_lib/_basic.py
def reset(function: Callable[..., None]) -> Callable[..., None]: ...
def transform_coords(old_coords: Tuple[int, int], new_coords: Tuple[int, int]) -> Tuple[int, float]: ...
def transform_line_coords(old_coords: Tuple[int, int], new_coords: Tuple[int, int]) -> Tuple[int, float]: ...
def transform_line_sequence(point_storage: Iterable) -> Tuple[(int, float), (int, float), (int, float), (int, float)]: ...
def detect_object(event: Event, canvas: CustomCanvas) -> [str, None]: ...
def select_style(italicB: bool, boldB: bool, family: str, size: str) -> Font: ...


# graphic_lib/_draw.py
class Draw:
    def __init__(self, root: Tk, event: Event, canvas: CustomCanvas) -> None: ...
    def point(self, *, size: (int, float) = DEFAULT_BRUSH_SIZE, color: str = DEFAULT_FIRST_COLOR, debug_mode: bool = False) -> None: ...
    def line(self, *, thickness: (int, float)= DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR, arrow: bool = False) -> None: ...
    def oval(self, *, thickness: (int, float) = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None: ...
    def rectangle(self, *, thickness: (int, float)= DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None: ...
    def polygon(self, *, thickness: (int, float) = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None: ...
    def text_creation(self) -> None: ...
    def coordinate_plane(self, *, thickness: (int, float) = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None: ...
    def move(self) -> None: ...
    def fill_objects(self, *, color: str = DEFAULT_CHANGE_COLOR) -> None: ...
    def thickness_objects(self, *, thickness: (int, float) = DEFAULT_THICKNESS) -> None: ...
    def outline_color_objects(self, *, color: str = DEFAULT_CHANGE_COLOR) -> None: ...
    def quick_eraser(self) -> None: ...
    def on_canvas(self) -> None: ...
    def undo(self) -> None: ...


# graphic_lib/_events.py
class Events:
    def __init__(self, root: Tk, used_events: Tuple[str], canvas: CustomCanvas) -> None: ...
    def event_btnClear(self) -> None: ...
    def event_btnBrush(self, *, size: (int, float) = DEFAULT_BRUSH_SIZE, color: str = DEFAULT_FIRST_COLOR, debug_mode: bool = False) -> None: ...
    def event_btnCreateLine(self, *, thickness: (int, float) = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None: ...
    def event_btnCreateOval(self, *, thickness: (int, float) = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None: ...
    def event_btnCreateRectangle(self, *, thickness: (int, float) = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None: ...
    def event_btnCreatePolygon(self, *, thickness: (int, float) = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None:  ...
    def event_btnCreateText(self) -> None: ...
    def event_btnCreateVector(self, *, thickness: (int, float) = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None: ...
    def event_btnCreateCoordinatePlane(self, *, thickness: (int, float) = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None: ...
    def event_undo(self, event: Event) -> None: ...
    def event_move(self, *, mouse_speed: int = DEFAULT_MOUSE_SPEED) -> None: ...
    def event_btnFill(self, *, color: str = DEFAULT_CHANGE_COLOR) -> None: ...
    def event_btnThickness(self, *, thickness: (int, float) = DEFAULT_THICKNESS) -> None: ...
    def event_btnOutlineColor(self, *, color: str = DEFAULT_CHANGE_COLOR) -> None: ...
    def event_btnQuickEraser(self) -> None: ...
    def event_onCanvas(self) -> None: ...

# graphic_lib/_custom_windows.py
class TextSettingsWindow(Toplevel):
    def __init__(self, root: Tk, *, text: str, family: str, size: str, italic: bool, bold: bool, color: str, **kwargs) -> None:
        super().__init__()
        ...
    def choose_color(self) -> None: ...
    def submit(self) -> None: ...
    def get_data(self) -> tuple: ...


""" ============= image_lib ============ """


# image_lib/_image_processing.py
def random_color() -> str: ...

class Img:
    def __init__(self, root: Tk, canvas: CustomCanvas) -> None: ...
    def set_image(self) -> None: ...
    def get_info(self) -> None: ...
    def save_image(self) -> None: ...
    def return_image(self) -> None: ...
    def grab(self, event: Event) -> None: ...
    def drag(self, event: Event) -> None: ...
    def zoom(self, event: Event) -> None: ...
    def zoom_in(self, event: Event) -> None: ...
    def zoom_off(self, event: Event) -> None: ...
    def redraw(self, direction: str = "in") -> None: ...
    def apply_filter_1(self, f: StringVar) -> None: ...
    def apply_filter_2(self, f: StringVar, per: Scale, event: Event) -> None: ...
    def apply_filter_3(self, f: StringVar) -> None: ...
    def apply_filter_4(self) -> None: ...
    def change_layers(self, red: Scale, green: Scale, blue: Scale, event: Event) -> None: ...
    def normalize_image(self) -> None: ...
    def append_image(self) -> None: ...
    def reflect_image(self, direction: str) -> None:  ...
    def rotate_image(self, direction: str) -> None: ...

# image_lib/_compress_window.py
class CompressWindow(Toplevel):
    def __init__(self, root: Canvas) -> None:
        super().__init__()
        ...
    def __submit(self) -> None: ...
    def open(self) -> str: ...