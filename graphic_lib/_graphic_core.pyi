""" Type hintings """


from tkinter import Event, Canvas, Tk
from typing import (
    Callable,
    Tuple,
    Iterable
)


# _defaults.py
DEFAULT_USED_EVENTS: Tuple[str]
DEFAULT_FIRST_COLOR: str
DEFAULT_SECOND_COLOR: (None, str)
DEFAULT_THICKNESS: int
DEFAULT_BRUSH_SIZE: int
DEFAULT_ERASER_SIZE: int
DEFAULT_MOUSE_SPEED: int
DEFAULT_CANVAS_W: int
DEFAULT_CANVAS_H: int
DEFAULT_CANVAS_BG: str


# _custom_objects.py
class CustomCanvas(Canvas):
    old_point: (None, Tuple[int, int])
    obj_oval: (None, int)
    obj_line: (None, int)
    obj_rectangle: (None, int)
    line_sequences: list
    obj_storage: dict = {}
    obj_tag: (None, str)


# _basic.py
def reset(function: Callable[..., None]) -> Callable[..., None]: ...
def transform_coords(old_coords: Tuple[int, int], new_coords: Tuple[int, int]) -> Tuple[int, float]: ...
def transform_line_coords(old_coords: Tuple[int, int], new_coords: Tuple[int, int]) -> Tuple[int, float]: ...
def transform_brush_sequence(point_storage: Iterable) -> Tuple[(int, float), (int, float), (int, float), (int, float)]: ...
def detect_object(event: Event, canvas: CustomCanvas) -> [str, None]: ...


# _draw.py
class Draw:
    def __init__(self, event: Event, canvas: CustomCanvas) -> None: ...
    def point(self, *, size: int = DEFAULT_BRUSH_SIZE, color: str = DEFAULT_FIRST_COLOR, eraser: bool = False, debug_mode: bool = False) -> None: ...
    def line(self, *, thickness: int = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None: ...
    def oval(self, *, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_FIRST_COLOR, outcolor: str = DEFAULT_SECOND_COLOR) -> None: ...
    def rectangle(self, *, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_FIRST_COLOR, outcolor: str = DEFAULT_SECOND_COLOR) -> None: ...
    def move(self, *, mouse_speed: int =  DEFAULT_MOUSE_SPEED) -> None: ...


# _events.py
class Events:
    def __init__(self, root: Tk, used_events: Tuple[str], canvas: CustomCanvas) -> None: ...
    def event_btnClear(self) -> None: ...
    def event_btnBrush(self, *, size: int = DEFAULT_BRUSH_SIZE, color: str = DEFAULT_FIRST_COLOR, debug_mode: bool = False) -> None: ...
    def event_btnCreateLine(self, *, thickness: int = DEFAULT_THICKNESS, color: str = DEFAULT_FIRST_COLOR) -> None: ...
    def event_btnCreateOval(self, *, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None: ...
    def event_btnCreateRectangle(self, *, thickness: int = DEFAULT_THICKNESS, bgcolor: str = DEFAULT_SECOND_COLOR, outcolor: str = DEFAULT_FIRST_COLOR) -> None: ...
    def event_undo(self) -> None: ...
    def event_move(self, *, mouse_speed: int = DEFAULT_MOUSE_SPEED) -> None: ...
    def event_btnEraser(self, *, size: int = DEFAULT_ERASER_SIZE) -> None: ...