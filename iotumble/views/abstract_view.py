from tkinter import EventType

from abc import ABC, abstractmethod


class AbstractView(ABC):
    primary_bg = "#333333"
    secondary_bg = "#2B2B2B"
    tertiary_bg = "#3F3F3F"
    highlight_bg = "#232323"
    primary_fg = "#976FFF"
    secondary_fg = "#4F3A86"
    tertiary_fg = "#C8B3FF"
    font = "Helvetica"

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @staticmethod
    def open(root):
        root.icon.bind("<Map>", lambda e: root.minimize_window(root, e))
        root.icon.bind("<Unmap>", lambda e: root.minimize_window(root, e))
        root.deiconify()

    @staticmethod
    def set_geometry(root, width, height):
        x_coord = int((root.winfo_screenwidth() / 2) - (width / 2))
        y_coord = int((root.winfo_screenheight() / 2) - (height / 2))
        root.geometry(f"{width}x{height}+{x_coord}+{y_coord}")

    @staticmethod
    def pressed_window(root, pressed, event):
        if pressed:
            root.x = event.x
            root.y = event.y
        else:
            root.x = None
            root.y = None

    @staticmethod
    def move_window(root, event):
        offset_x = event.x - root.x
        offset_y = event.y - root.y
        x_coord = root.winfo_x() + offset_x
        y_coord = root.winfo_y() + offset_y
        root.geometry(f"+{x_coord}+{y_coord}")

    @staticmethod
    def minimize_window(root, event):
        if event.type == EventType.Map:
            root.deiconify()
        else:
            root.withdraw()
